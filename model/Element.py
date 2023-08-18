from abc import ABC, abstractmethod

class Element(ABC):

    # TODO Properties x_start, x_end, is_spot, is_segment

    @abstractmethod
    def value_at(self, x):
        pass
