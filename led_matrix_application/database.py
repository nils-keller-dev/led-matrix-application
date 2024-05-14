import json
from controller import led_matrix_controller
from deepmerge import always_merger

class Database:
  def get_state(self) -> dict:
    with open('state.json', 'r') as f:
      state = json.load(f)
    return state

  def set_state(self, state: dict):
    with open('state.json', 'w') as f:
      json.dump(state, f)

  def patch_state(self, new_data: dict):
    state = self.get_state()
    state = always_merger.merge(state, new_data)
    led_matrix_controller.update_state(state)
    self.set_state(state)