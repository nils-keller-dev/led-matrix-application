import time

from mode.abstract_mode import AbstractMode

class IdleMode(AbstractMode):
    def start(self, matrix):
        matrix.Clear()

    def update_settings(self, settings):
        pass

    def update_display(self):
        time.sleep(1)
