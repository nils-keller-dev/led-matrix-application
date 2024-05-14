from RGBMatrixEmulator import RGBMatrix, RGBMatrixOptions
from mode.idle_mode import IdleMode
from mode.clock_mode import ClockMode
from mode.text_mode import TextMode
from mode.music_mode import MusicMode
from mode.image_mode import ImageMode

class LEDMatrixController:
    def __init__(self):
        options = RGBMatrixOptions()
        options.rows = 64
        options.cols = 64
        options.brightness = 50 
        self.matrix = RGBMatrix(options=options)
        self.modes = {
            'idle': IdleMode(),
            'clock': ClockMode(),
            'text': TextMode(),
            'music': MusicMode(),
            'image': ImageMode()
        }
        self.current_mode = None
        self.mode_started = False

    def switch_mode(self, mode_name):
        if self.current_mode == self.modes[mode_name]:
            return
        self.mode_started = False
        self.current_mode = self.modes[mode_name]
        self.current_mode.start(self.matrix)
        self.mode_started = True

    def update_settings(self, settings):
        self.current_mode.update_settings(settings)

    def update_display(self):
        if not self.mode_started:
            return
        self.current_mode.update_display()
    
    def update_state(self, state):
        self.matrix.brightness = state['global']['brightness']
        mode_name = state['global']['mode']
        self.switch_mode(mode_name)
        if mode_name in state:
            self.update_settings(state[mode_name])

    def run(self):
        while True:
            self.update_display()
