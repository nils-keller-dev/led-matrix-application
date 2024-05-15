import json

from controller import led_matrix_controller


def custom_merge(dict1, dict2):
    for key, value in dict2.items():
        if isinstance(value, dict):
            dict1[key] = custom_merge(dict1.get(key, {}), value)
        elif isinstance(value, list):
            dict1[key] = value[:]
        else:
            dict1[key] = value
    return dict1


class Database:
    def get_state(self) -> dict:
        with open("state.json", "r", encoding="utf-8") as f:
            state = json.load(f)
        return state

    def set_state(self, state: dict):
        with open("state.json", "w", encoding="utf-8") as f:
            json.dump(state, f)

    def patch_state(self, new_data: dict):
        state = self.get_state()
        state = custom_merge(state, new_data)
        led_matrix_controller.update_state(state)
        self.set_state(state)
