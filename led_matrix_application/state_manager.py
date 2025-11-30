import threading

from database import Database
from led_matrix_controller import LEDMatrixController
from solar_time_service import SolarTimeService


class StateManager:
    def __init__(self, database: Database, led_controller: LEDMatrixController):
        self.database = database
        self.led_controller = led_controller
        self._lock = threading.Lock()
        self.solar_service = SolarTimeService()
        self.led_controller.update_state(self.database.get_state())

    def get_state(self) -> dict:
        with self._lock:
            return self.database.get_state()

    def update_state(self, new_data: dict):
        with self._lock:
            self.database.patch_state(new_data)

            current_state = self.database.get_state()["global"]["brightness"]
            new_state = new_data["global"]["brightness"]

            is_daytime = self.solar_service.is_daytime()

            if "night" in new_state and not is_daytime:
                self._database_patch_brightness_key("current", new_state["night"])
            elif "day" in new_state and is_daytime:
                self._database_patch_brightness_key("current", new_state["day"])
            elif "adaptive" in new_state and new_state["adaptive"] and is_daytime:
                self._database_patch_brightness_key("day", current_state["current"])
            elif "adaptive" in new_state and new_state["adaptive"] and not is_daytime:
                self._database_patch_brightness_key("current", current_state["night"])

            self.led_controller.update_state(self.database.get_state())

    def _database_patch_brightness_key(self, key: str, value: int):
        self.database.patch_state(
            {
                "global": {
                    "brightness": {
                        key: value,
                    }
                }
            }
        )
