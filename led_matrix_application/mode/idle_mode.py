import time

from mode.abstract_mode import AbstractMode


class IdleMode(AbstractMode):
    def __init__(self, matrix):
        super().__init__(matrix)
        self.offscreen_canvas = matrix.CreateFrameCanvas()

    def start(self):
        self.offscreen_canvas.Clear()
        self.offscreen_canvas = self.matrix.SwapOnVSync(self.offscreen_canvas)

    def stop(self):
        pass

    def update_settings(self, _):
        pass

    def update_display(self):
        time.sleep(0.1)
