from .Element import Element


class Spot(Element):

    def __init__(self, x, y):
        self.x_start = x
        self.y = y
        self.is_segment = False
        self.is_spot = True
        self.x_end = x

    def value_at(self, x):
        if x == self.x_start:
            return self.y
        else:
            return None

