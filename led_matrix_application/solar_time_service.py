import logging
import os
import threading
import time
from datetime import datetime
from datetime import time as time_type
from typing import Optional

import pyowm

logger = logging.getLogger(__name__)


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
            logger.warning("Retrying solar times fetch in 10 seconds...")
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
            logger.info(
                "Fetched solar times - Sunrise: %s, Sunset: %s",
                self._sunrise_time,
                self._sunset_time,
            )
        except Exception as e:
            logger.error("Error fetching solar times: %s", e, exc_info=True)

    def is_daytime(self) -> bool:
        return self._sunrise_time <= datetime.now().time() < self._sunset_time

    @property
    def sunrise_time(self) -> Optional[time_type]:
        return self._sunrise_time

    @property
    def sunset_time(self) -> Optional[time_type]:
        return self._sunset_time
