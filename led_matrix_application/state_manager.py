from database import Database


class StateManager:
    def __init__(self, database, led_controller):
        self.db = database
        self.led_controller = led_controller
        self.led_controller.update_state(self.db.get_state())

    def get_state(self) -> dict:
        return self.db.get_state()

    def update_state(self, new_data: dict):
        self.db.patch_state(new_data)
        self.led_controller.update_state(self.db.get_state())
