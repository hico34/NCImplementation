from .Spot import Spot
from .Segment import Segment
from fractions import Fraction


class Piece:
    def __init__(self, x_start, y_spot, y_segment, x_end, slope):
        self.x_start = Fraction(x_start)
        self.y_spot = Fraction(y_spot)
        self.y_segment = Fraction(y_segment)
        self.x_end = Fraction(x_end)
        self.slope = Fraction(slope)

    def value_at(self, x):
        if x == self.x_start:
            return self.y_spot
        elif self.x_start < x < self.x_end:
            return (x - self.x_start) * self.slope + self.y_segment
        else:
            return None

    # Calculates right limit if x = x_start, left limit if x = x_end, normal value else
    def lim_value_at(self, x):
        if x == self.x_start:
            return self.y_segment
        elif x == self.x_end:
            return self.y_segment + self.slope * (x - self.x_start)
        else:
            return self.value_at(x)

    def decompose(self):
        spot = Spot(self.x_start, self.y_spot)
        segment = Segment(self.x_start, self.y_segment, self.x_end, self.slope)
        return spot, segment

    # Looks for the index of the piece defined on x via binary search
    # index_offset should always be 0 when not called recursively
    @staticmethod
    def index_of_piece_at(pieces, x, index_offset=0):
        middle_index = len(pieces) // 2
        left_pieces = pieces[0:middle_index]
        middle_piece = pieces[middle_index]
        right_pieces = pieces[middle_index+1:]
        if middle_piece.x_start <= x < middle_piece.x_end:
            return index_offset + middle_index
        # If there are no pieces left to search, return None
        if x < middle_piece.x_start:
            if len(left_pieces) == 0:
                return None
            return Piece.index_of_piece_at(left_pieces, x, index_offset)
        if x >= pieces[middle_index].x_end:
            if len(right_pieces) == 0:
                return None
            return Piece.index_of_piece_at(right_pieces, x, index_offset + middle_index + 1)

    def __str__(self):
        return "{x_start: " + str(self.x_start) + " , y_spot: " + str(self.y_spot) + " , y_segment: " + str(self.y_segment) + " , slope: " + str(self.slope) + " , x_end: " + str(self.x_end) + "}"

    def __eq__(self, other):
        if not isinstance(other, Piece):
            return False
        return self.x_start == other.x_start and self.y_spot == other.y_spot and self.y_segment == other.y_segment and self.x_end == other.x_end and self.slope == other.slope
