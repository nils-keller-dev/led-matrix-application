from mode.abstract_mode import AbstractMode
from datetime import date, datetime
import time
from RGBMatrixEmulator import graphics
import pytz

class ClockMode(AbstractMode):
    def start(self, matrix):
        self.matrix = matrix
        self.timezone = pytz.timezone("Europe/Berlin")
        self.font = graphics.Font()
        self.font.LoadFont("fonts/9x18.bdf")
        self.offscreen_canvas = matrix.CreateFrameCanvas()

    def update_settings(self, settings):
        self.settings = settings

    def update_display(self):
        self.offscreen_canvas.Clear()
        awareTime = datetime.now(self.timezone)
        if (time.mktime(awareTime.timetuple()) % 2 == 0):
            displayTime = awareTime.strftime("%H %M")
        else:
            displayTime = awareTime.strftime("%H:%M")

        displayDate = date.today().strftime("%d.%b")
        graphics.DrawText(self.offscreen_canvas, self.font, 10, 16, graphics.Color(*self.settings['color']), displayTime)
        graphics.DrawText(self.offscreen_canvas, self.font, 5, 58, graphics.Color(*self.settings['color']), displayDate)
        time.sleep(0.1)
        self.offscreen_canvas = self.matrix.SwapOnVSync(self.offscreen_canvas)

