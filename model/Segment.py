from .Element import Element

class Segment(Element):
    def __init__(self, x_start, y_segment, x_end, slope):
        self.x_start = x_start
        self.y_segment = y_segment
        self.slope = slope
        self.x_end = x_end
        self.is_segment = True
        self.is_spot = False

    def value_at(self, x):
        if self.x_start < x < self.x_end:
            return (x - self.x_start) * self.slope + self.y_segment
        else:
            return None

    def lim_value_at(self, x):
        if x == self.x_start:
            return self.y_segment
        elif x == self.x_end:
            return self.y_segment + self.slope * (x - self.x_start)
        else:
            return self.value_at(x)

    def split_at(self, x):
        left_segment = Segment(self.x_start, self.y_segment, x, self.slope)
        right_segment = Segment(x, self.value_at(x), self.x_end, self.slope)
        return left_segment, right_segment

