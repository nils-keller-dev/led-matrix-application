from abc import ABC, abstractmethod


class AbstractMode(ABC):
    def __init__(self):
        self.matrix = None
        self.settings = None

    @abstractmethod
    def start(self, matrix):
        pass

    @abstractmethod
    def update_settings(self, settings):
        pass

    @abstractmethod
    def update_display(self):
        pass
