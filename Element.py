class Element:
    def __init__(self, x_start, y_spot, y_segment, x_end, slope):
        self.x_start = x_start
        self.y_spot = y_spot
        self.y_segment = y_segment
        self.slope = slope
        self.x_end = x_end

    def __str__(self):
        return "{x_start: " + str(self.x_start) + " , y_spot: " + str(self.y_spot) + " , y_segment: " + str(self.y_segment) + " , slope: " + str(self.slope) + " , x_end: " + str(self.x_end) + "}"

    def value_at(self, x):
        if x == self.x_start:
            return self.y_spot
        elif self.x_start < x < self.x_end:
            return (x - self.x_start) * self.slope + self.y_segment
        else:
            return None
