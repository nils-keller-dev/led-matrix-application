import os
import time
from datetime import date, datetime

import pyowm
import pytz
from dotenv import load_dotenv
from mode.abstract_mode import AbstractMode
from PIL import Image
from RGBMatrixEmulator import graphics


class ClockMode(AbstractMode):
    def __init__(self):
        super().__init__()
        self.location = None
        self.timezone = None
        self.font = None
        self.weather_manager = None
        self.offscreen_canvas = None
        self.last_refresh = None
        self.icon = None
        self.temperature = None

    def start(self, matrix):
        self.matrix = matrix
        load_dotenv()
        self.location = os.getenv("LOCATION")
        self.timezone = pytz.timezone(os.getenv("TIMEZONE"))
        self.font = graphics.Font()
        self.font.LoadFont("fonts/9x18.bdf")
        owm = pyowm.OWM(os.getenv("OWM_API_KEY"))
        self.weather_manager = owm.weather_manager()
        self.offscreen_canvas = matrix.CreateFrameCanvas()
        self.refresh_weather_date()
        self.last_refresh = time.time()

    def update_settings(self, settings):
        self.settings = settings

    def update_display(self):
        self.offscreen_canvas.Clear()
        display_color = graphics.Color(*self.settings["color"])
        aware_time = datetime.now(self.timezone)
        time_hours = aware_time.strftime("%H")
        time_minutes = aware_time.strftime("%M")

        graphics.DrawText(
            self.offscreen_canvas, self.font, 10, 16, display_color, time_hours
        )
        if time.mktime(aware_time.timetuple()) % 2 == 0:
            graphics.DrawText(
                self.offscreen_canvas, self.font, 27, 15, display_color, ":"
            )
        graphics.DrawText(
            self.offscreen_canvas, self.font, 36, 16, display_color, time_minutes
        )

        display_date = date.today().strftime("%d %b")
        graphics.DrawText(
            self.offscreen_canvas, self.font, 5, 58, display_color, display_date
        )
        graphics.DrawText(self.offscreen_canvas, self.font, 20, 58, display_color, ".")

        self.draw_icon(4, 24)
        graphics.DrawText(
            self.offscreen_canvas, self.font, 24, 37, display_color, self.temperature
        )

        self.offscreen_canvas = self.matrix.SwapOnVSync(self.offscreen_canvas)

        current_time = time.time()
        if current_time - self.last_refresh >= 60:
            self.refresh_weather_date()
            self.last_refresh = current_time

    def refresh_weather_date(self):
        try:
            data = self.weather_manager.weather_at_place(self.location).weather
            path = f"icons/clock/{data.weather_icon_name}.png"
            with Image.open(path) as img:
                self.icon = img.copy()
            self.temperature = f"{int(round(data.temperature('celsius')['temp']))}°C"
        except Exception as e:
            print(f"Error in refresh_weather_date: {e}")

    def draw_icon(self, x, y):
        width = self.icon.size[0]
        color = tuple(self.settings["color"])
        for index, pixel in enumerate(self.icon.getdata()):
            if pixel[0] == 255:
                self.offscreen_canvas.SetPixel(
                    x + (index % width), y + index // width, *color
                )
