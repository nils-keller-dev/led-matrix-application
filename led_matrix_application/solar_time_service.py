import os
import threading
import time
from datetime import datetime
from datetime import time as time_type
from typing import Optional

import pyowm


class SolarTimeService:
    _instance = None
    _initialized = False

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance

    def __init__(self):
        if self._initialized:
            return

        self._sunrise_time: Optional[time_type] = None
        self._sunset_time: Optional[time_type] = None
        self.location = os.getenv("LOCATION")
        owm = pyowm.OWM(os.getenv("OWM_API_KEY"))
        self.weather_manager = owm.weather_manager()

        self._fetch_solar_times()
        while self.sunrise_time is None or self.sunset_time is None:
            print("Retrying solar times fetch in 10 seconds...")
            time.sleep(10)
            self._fetch_solar_times()

        threading.Thread(target=self.periodic_fetch, daemon=True).start()
        self._initialized = True

    def periodic_fetch(self):
        while True:
            time.sleep(12 * 60 * 60)
            self._fetch_solar_times()

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

    def is_daytime(self) -> bool:
        return self._sunrise_time <= datetime.now().time() < self._sunset_time

    @property
    def sunrise_time(self) -> Optional[time_type]:
        return self._sunrise_time

    @property
    def sunset_time(self) -> Optional[time_type]:
        return self._sunset_time
