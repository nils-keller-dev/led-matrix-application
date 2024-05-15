import time

from mode.abstract_mode import AbstractMode
from PIL import Image


class ImageMode(AbstractMode):
    def __init__(self, matrix):
        super().__init__(matrix)
        self.offscreen_canvas = matrix.CreateFrameCanvas()

    def start(self):
        self.matrix.Clear()

    def update_settings(self, settings):
        img = Image.open(f"images/{settings['image']}")
        img.thumbnail((64, 64))
        offset = (64 - img.size[0]) // 2, (64 - img.size[1]) // 2
        self.matrix.Clear()
        self.matrix.SetImage(img.convert("RGB"), offset[0], offset[1], False)

    def update_display(self):
        time.sleep(0.1)
