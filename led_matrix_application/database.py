import json

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
    state.update(new_data)
    self.set_state(state)