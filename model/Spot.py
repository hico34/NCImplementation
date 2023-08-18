class Spot:
    def __init__(self, x, y):
        self.x_start = x
        self.y = y

    def value_at(self, x):
        if x == self.x_start:
            return self.y
        else:
            return None