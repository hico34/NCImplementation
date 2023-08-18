# Describes multiple elements (spots or segments) that are defined over the same interval

class ElementCollection:
    def __init__(self, elements, x_start, x_end):
        self.elements = elements
        self.x_start = x_start
        self.x_end = x_end
