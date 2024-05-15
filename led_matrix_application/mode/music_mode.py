from mode.abstract_mode import AbstractMode


class MusicMode(AbstractMode):
    def start(self):
        pass

    def update_settings(self, settings):
        self.settings = settings

    def update_display(self):
        self.matrix.Fill(0, 0, 255)
