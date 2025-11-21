import json
import os


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
    def __init__(self):
        if not os.path.exists("state.json"):
            default_state = {
                "global": {"mode": "idle", "brightness": 50},
                "text": {
                    "text": "",
                    "align": "left",
                    "speed": 0,
                    "size": 1,
                    "color": [255, 255, 255],
                },
                "image": {"image": ""},
                "clock": {
                    "color": [255, 255, 255],
                    "backgroundColor": [0, 0, 0],
                    "backgroundBrightness": 0,
                },
                "music": {"fullscreen": False},
            }
            with open("state.json", "w", encoding="utf-8") as f:
                json.dump(default_state, f, indent=2)

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
        self.set_state(state)
