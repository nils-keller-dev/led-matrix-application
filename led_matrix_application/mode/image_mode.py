import time

from mode.abstract_mode import AbstractMode
from PIL import Image, ImageSequence


class ImageMode(AbstractMode):
    def __init__(self, matrix):
        super().__init__(matrix)
        self.offscreen_canvas = matrix.CreateFrameCanvas()
        self.image_frames = []
        self.current_frame = 0
        self.offset = (0, 0)

    def start(self):
        self.matrix.Clear()

    def update_settings(self, settings):
        img = Image.open(f"images/{settings['image']}")
        self.current_frame = 0
        if img.format == "GIF":
            self.image_frames = [
                self.process_frame(frame.copy())
                for frame in ImageSequence.Iterator(img)
            ]
        else:
            self.image_frames = [self.process_frame(img)]

        first_frame = self.image_frames[0]
        self.offset = (64 - first_frame.size[0]) // 2, (64 - first_frame.size[1]) // 2
        self.matrix.Clear()
        self.matrix.SetImage(first_frame, self.offset[0], self.offset[1], False)

    def update_display(self):
        time.sleep(0.1)
        if not self.image_frames:
            return
        img = self.image_frames[self.current_frame]
        self.offscreen_canvas.Clear()
        self.offscreen_canvas.SetImage(img, self.offset[0], self.offset[1], False)
        self.current_frame = (self.current_frame + 1) % len(self.image_frames)
        self.offscreen_canvas = self.matrix.SwapOnVSync(self.offscreen_canvas)

    def process_frame(self, frame):
        frame.thumbnail((64, 64))
        return frame.convert("RGB")
