from mode.abstract_mode import AbstractMode
from RGBMatrixEmulator import graphics


class TextMode(AbstractMode):
    def __init__(self, matrix):
        super().__init__(matrix)
        self.font = graphics.Font()
        self.size = None
        self.offscreen_canvas = matrix.CreateFrameCanvas()

    def start(self):
        pass

    def update_settings(self, settings):
        self.settings = settings
        if self.size != self.settings["size"]:
            self.font.LoadFont(f"fonts/tamzen/{self.settings['size']}.bdf")
            self.size = self.settings["size"]

    def update_display(self):
        self.offscreen_canvas.Clear()

        one_char_width = self.font.CharacterWidth(0x0020)
        split_text = self.settings["text"].split(" ")

        line_list = []
        text_line = ""
        max_length = 64 // one_char_width

        for i, text in enumerate(split_text):
            while len(text) > max_length:
                first_half = text[:max_length]
                text = text[max_length:]
                text_line += first_half + " "
                line_list.append(text_line)
                text_line = ""
            if one_char_width * len(text_line + text) < 64:
                text_line += text + " "
            else:
                line_list.append(text_line)
                text_line = text + " "

        line_list.append(text_line)

        total_height = len(line_list) * self.font.height
        offset_top = max((64 - total_height) // 2, 0)

        for i, line in enumerate(line_list):
            trimmed_line = line[:-1]
            offset_left = 0
            if self.settings["align"] == "center":
                width = one_char_width * len(trimmed_line)
                offset_left = (64 - width) // 2

            graphics.DrawText(
                self.offscreen_canvas,
                self.font,
                offset_left,
                offset_top + ((i + 1) * self.font.height) - self.size,
                graphics.Color(*self.settings["color"]),
                trimmed_line,
            )

        self.offscreen_canvas = self.matrix.SwapOnVSync(self.offscreen_canvas)
