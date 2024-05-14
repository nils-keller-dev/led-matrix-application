from mode.abstract_mode import AbstractMode

class TextMode(AbstractMode):
    def start(self, matrix):
        self.matrix = matrix

    def update_settings(self, settings):
        self.settings = settings

    def update_display(self):
        self.matrix.Fill(255, 0, 0)
