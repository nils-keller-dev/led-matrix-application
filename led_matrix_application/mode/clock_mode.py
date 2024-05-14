from datetime import date, datetime
import os
import time

from PIL import Image
import pyowm
from dotenv import load_dotenv
import pytz
from RGBMatrixEmulator import graphics

from mode.abstract_mode import AbstractMode

class ClockMode(AbstractMode):
    def start(self, matrix):
        self.matrix = matrix
        load_dotenv()
        self.location = os.getenv('LOCATION')
        self.timezone = pytz.timezone(os.getenv('TIMEZONE'))
        self.font = graphics.Font()
        self.font.LoadFont("fonts/9x18.bdf")
        owm = pyowm.OWM(os.getenv('OWM_API_KEY'))
        self.weather_manager = owm.weather_manager()
        self.offscreen_canvas = matrix.CreateFrameCanvas()
        self.refreshWeatherDate()
        self.last_refresh = time.time()

    def update_settings(self, settings):
        self.settings = settings

    def update_display(self):
        self.offscreen_canvas.Clear()
        displayColor = graphics.Color(*self.settings['color'])
        awareTime = datetime.now(self.timezone)
        timeHours = awareTime.strftime("%H")
        timeMinutes = awareTime.strftime("%M")
        
        graphics.DrawText(self.offscreen_canvas, self.font, 10, 16, displayColor, timeHours)
        if (time.mktime(awareTime.timetuple()) % 2 == 0):
            graphics.DrawText(self.offscreen_canvas, self.font, 27, 15, displayColor, ":")
        graphics.DrawText(self.offscreen_canvas, self.font, 36, 16, displayColor, timeMinutes)

        displayDate = date.today().strftime("%d %b")
        graphics.DrawText(self.offscreen_canvas, self.font, 5, 58, displayColor, displayDate)
        graphics.DrawText(self.offscreen_canvas, self.font, 20, 58, displayColor, ".")

        self.drawIcon(4, 24)
        graphics.DrawText(self.offscreen_canvas, self.font, 24, 37, displayColor, self.temperature)
        
        self.offscreen_canvas = self.matrix.SwapOnVSync(self.offscreen_canvas)

        current_time = time.time()
        if current_time - self.last_refresh >= 60:
            self.refreshWeatherDate()
            self.last_refresh = current_time

    def refreshWeatherDate(self):
        try:
            data = self.weather_manager.weather_at_place(self.location).weather
            path = f"icons/clock/{data.weather_icon_name}.png"
            with Image.open(path) as img:
                self.icon = img.copy()
            self.temperature = f"{int(round(data.temperature('celsius')['temp']))}°C"
        except Exception as e:
            print(f"Error fetching temperature data: {e}")

    def drawIcon(self, x, y):
        width = self.icon.size[0]
        color = tuple(self.settings['color'])
        for index, pixel in enumerate(self.icon.getdata()):
            if pixel[0] == 255:
                self.offscreen_canvas.SetPixel(x + (index % width), y + index // width, *color)
