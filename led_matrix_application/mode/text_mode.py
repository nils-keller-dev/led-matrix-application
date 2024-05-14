from mode.abstract_mode import AbstractMode

class TextMode(AbstractMode):
    def start(self):
        pass

    def stop(self):
        pass

    def update_settings(self, settings):
        self.settings = settings

    def update_display(self, matrix):
        matrix.Fill(255, 0, 0)
