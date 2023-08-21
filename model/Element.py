from abc import ABC, abstractmethod

class Element(ABC):

    @abstractmethod
    def value_at(self, x):
        pass
