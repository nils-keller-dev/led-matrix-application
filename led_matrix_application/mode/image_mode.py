import time

from mode.abstract_mode import AbstractMode
from PIL import Image, ImageSequence


class ImageMode(AbstractMode):
    def __init__(self, matrix):
        super().__init__(matrix)
        self.offscreen_canvas = matrix.CreateFrameCanvas()
        self.image_frames = []
        self.frame_durations = []
        self.current_frame = 0
        self.offset = (0, 0)

    def start(self):
        self.matrix.Clear()

    def update_settings(self, settings):
        img = Image.open(f"images/{settings['image']}")
        self.current_frame = 0
        if img.format == "GIF":
            self.image_frames = []
            self.frame_durations = []
            for frame in ImageSequence.Iterator(img):
                self.image_frames.append(self.process_frame(frame.copy()))
                self.frame_durations.append(frame.info.get("duration", 100))
        else:
            self.image_frames = [self.process_frame(img)]
            self.frame_durations = [100]

        first_frame = self.image_frames[0]
        self.offset = (64 - first_frame.size[0]) // 2, (64 - first_frame.size[1]) // 2
        self.matrix.Clear()
        self.matrix.SetImage(first_frame, self.offset[0], self.offset[1], False)

    def update_display(self):
        if not self.image_frames:
            return
        start_time = time.time()
        img = self.image_frames[self.current_frame]
        self.offscreen_canvas.Clear()
        self.offscreen_canvas.SetImage(img, self.offset[0], self.offset[1], False)
        self.current_frame = (self.current_frame + 1) % len(self.image_frames)
        self.offscreen_canvas = self.matrix.SwapOnVSync(self.offscreen_canvas)
        end_time = time.time()
        calculation_time = end_time - start_time
        sleep_time = max(
            self.frame_durations[self.current_frame] / 1000 - calculation_time, 0
        )
        time.sleep(sleep_time)

    def process_frame(self, frame):
        frame.thumbnail((64, 64))
        return frame.convert("RGB")
