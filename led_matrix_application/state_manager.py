from database import Database
from led_matrix_controller import LEDMatrixController


class StateManager:
    def __init__(self, database: Database, led_controller: LEDMatrixController):
        self.database = database
        self.led_controller = led_controller
        self.led_controller.update_state(self.database.get_state())

    def get_state(self) -> dict:
        return self.database.get_state()

    def update_state(self, new_data: dict):
        self.database.patch_state(new_data)
        self.led_controller.update_state(self.database.get_state())
