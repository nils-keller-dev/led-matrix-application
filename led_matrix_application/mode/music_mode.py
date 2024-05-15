import time

from mode.abstract_mode import AbstractMode
from PIL import Image


class MusicMode(AbstractMode):
    def __init__(self, matrix):
        super().__init__(matrix)
        self.logo = Image.open("icons/spotify.png")

    def start(self):
        self.matrix.Clear()
        self.matrix.SetImage(self.logo, 20, 20, False)

    def update_settings(self, _):
        pass

    def update_display(self):
        time.sleep(0.1)
