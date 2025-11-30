import os
import threading
import time
from datetime import datetime
from datetime import time as time_type
from datetime import timedelta

import pyowm
from state_manager import StateManager


class BrightnessScheduler:
    def __init__(self, state_manager: StateManager):
        self.state_manager = state_manager
        self._sunrise_time = None
        self._sunset_time = None

        self.location = os.getenv("LOCATION")
        owm = pyowm.OWM(os.getenv("OWM_API_KEY"))
        self.weather_manager = owm.weather_manager()

    def _fetch_solar_times(self):
        try:
            data = self.weather_manager.weather_at_place(self.location).weather
            sunrise_timestamp = data.sunrise_time()
            sunset_timestamp = data.sunset_time()

            self._sunrise_time = datetime.fromtimestamp(sunrise_timestamp).time()
            self._sunset_time = datetime.fromtimestamp(sunset_timestamp).time()
            print(
                f"Fetched solar times - Sunrise: {self._sunrise_time}, Sunset: {self._sunset_time}"
            )
        except Exception as e:
            print(f"Error fetching solar times: {e}")

    def _is_daytime(self) -> bool:
        return self._sunrise_time <= datetime.now().time() < self._sunset_time

    def _seconds_until(self, target_time: time_type) -> float:
        now = datetime.now()
        target = datetime.combine(now.date(), target_time)

        if target <= now:
            target += timedelta(days=1)

        return (target - now).total_seconds()

    def _update_brightness(self, is_daytime: bool):
        state = self.state_manager.get_state()
        brightness_config = state["global"]["brightness"]

        if not brightness_config["adaptive"]:
            print("Adaptive brightness is disabled; skipping update.")
            return

        target_brightness = brightness_config["day" if is_daytime else "night"]

        self.state_manager._internal_brightness_update(
            {"global": {"brightness": {"current": target_brightness}}}
        )
        print(f"Set brightness to {target_brightness}")

    def _on_sun_event(self, is_sunrise: bool):
        print(f"{'Sunrise' if is_sunrise else 'Sunset'} event triggered")
        self._update_brightness(is_sunrise)
        self._schedule_sun_event(is_sunrise)

    def _schedule_sun_event(self, is_sunrise: bool):
        delay = self._seconds_until(
            self._sunrise_time if is_sunrise else self._sunset_time
        )

        next_event = "sunrise" if is_sunrise else "sunset"
        print(f"Scheduling next {next_event} event in {delay/3600:.2f} hours")
        timer = threading.Timer(delay, self._on_sun_event, args=(is_sunrise,))
        timer.daemon = True
        timer.start()

    def run(self):
        self._fetch_solar_times()
        while self._sunrise_time is None or self._sunset_time is None:
            print("Retrying solar times fetch in 60 seconds...")
            time.sleep(60)
            self._fetch_solar_times()

        is_daytime = self._is_daytime()
        print(f"Initial time: {'Day' if is_daytime else 'Night'}")
        self._update_brightness(is_daytime)

        self._schedule_sun_event(is_sunrise=True)
        self._schedule_sun_event(is_sunrise=False)
        while True:
            time.sleep(12 * 60 * 60)
            self._fetch_solar_times()
