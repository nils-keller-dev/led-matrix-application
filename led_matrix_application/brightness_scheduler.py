import threading
from datetime import datetime
from datetime import time as time_type
from datetime import timedelta

from solar_time_service import SolarTimeService
from state_manager import StateManager


class BrightnessScheduler:
    def __init__(self, state_manager: StateManager):
        self.state_manager = state_manager
        self.solar_service = SolarTimeService()

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

        if is_daytime and brightness_config["current"] != brightness_config["night"]:
            print(
                "It is sunrise but current was manually changed during the night; skipping update."
            )
            return

        target_brightness = brightness_config["day" if is_daytime else "night"]
        new_state = {"global": {"brightness": {"current": target_brightness}}}

        self.state_manager.update_state(new_state)
        print(f"Set brightness to {target_brightness}")

    def _on_sun_event(self, is_sunrise: bool):
        print(f"{'Sunrise' if is_sunrise else 'Sunset'} event triggered")
        self._update_brightness(is_sunrise)
        self._schedule_sun_event(is_sunrise)

    def _schedule_sun_event(self, is_sunrise: bool):
        delay = self._seconds_until(
            self.solar_service.sunrise_time
            if is_sunrise
            else self.solar_service.sunset_time
        )

        next_event = "sunrise" if is_sunrise else "sunset"
        print(f"Scheduling next {next_event} event in {delay/3600:.2f} hours")
        timer = threading.Timer(delay, self._on_sun_event, args=(is_sunrise,))
        timer.daemon = True
        timer.start()

    def run(self):
        is_daytime = self.solar_service.is_daytime()
        print(f"Initial time: {'Day' if is_daytime else 'Night'}")
        self._update_brightness(is_daytime)

        self._schedule_sun_event(is_sunrise=True)
        self._schedule_sun_event(is_sunrise=False)
