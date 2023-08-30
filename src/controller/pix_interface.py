from abc import ABC, abstractmethod


class PixInterface(ABC):
    @abstractmethod
    def create_pix(self, value):
        pass

    @abstractmethod
    def is_done(self):
        pass
