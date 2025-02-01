import os
import time
from datetime import date, datetime

import pyowm
import pytz
from dotenv import load_dotenv
from mode.abstract_mode import AbstractMode
from PIL import Image
from utils import get_rgb_matrix

graphics = get_rgb_matrix().get("graphics")


class ClockMode(AbstractMode):
    def __init__(self, matrix):
        super().__init__(matrix)
        load_dotenv()
        self.location = os.getenv("LOCATION")
        self.timezone = pytz.timezone(os.getenv("TIMEZONE"))
        owm = pyowm.OWM(os.getenv("OWM_API_KEY"))
        self.weather_manager = owm.weather_manager()
        self.offscreen_canvas = None
        self.last_refresh = None
        self.icon = None
        self.temperature = None
        self.font = graphics.Font()
        self.font.LoadFont("fonts/clock.bdf")
        self.offscreen_canvas = matrix.CreateFrameCanvas()

    def start(self):
        self.refresh_weather_data()
        self.last_refresh = time.time()

    def stop(self):
        pass

    def update_settings(self, settings):
        self.settings = settings

    def update_display(self):
        self.offscreen_canvas.Clear()
        display_color = graphics.Color(*self.settings["color"])
        background_color = graphics.Color(*self.settings["backgroundColor"])
        aware_time = datetime.now(self.timezone)
        time_hours = aware_time.strftime("%H")
        time_minutes = aware_time.strftime("%M")

        for y in range(self.offscreen_canvas.height):
            graphics.DrawLine(
                self.offscreen_canvas,
                0,
                y,
                self.offscreen_canvas.width,
                y,
                background_color,
            )

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
            self.refresh_weather_data()
            self.last_refresh = current_time

        time.sleep(0.1)

    def refresh_weather_data(self):
        try:
            data = self.weather_manager.weather_at_place(self.location).weather
            path = f"icons/clock/{data.weather_icon_name}.png"
            with Image.open(path) as img:
                self.icon = img.copy()
            self.temperature = f"{int(round(data.temperature('celsius')['temp']))}°C"
        except Exception as e:
            print(f"Error in refresh_weather_data: {e}")

    def draw_icon(self, x, y):
        width = self.icon.size[0]
        color = tuple(self.settings["color"])
        for index, pixel in enumerate(self.icon.getdata()):
            if pixel[0] == 255:
                self.offscreen_canvas.SetPixel(
                    x + (index % width), y + index // width, *color
                )
