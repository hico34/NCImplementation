class Segment:
    def __init__(self, x_start, y_segment, x_end, slope):
        self.x_start = x_start
        self.y_segment = y_segment
        self.slope = slope
        self.x_end = x_end

    def value_at(self, x):
        if self.x_start < x < self.x_end:
            return (x - self.x_start) * self.slope + self.y_segment
        else:
            return None
