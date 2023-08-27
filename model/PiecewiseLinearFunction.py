import math
from .Piece import Piece
from fractions import Fraction


class PiecewiseLinearFunction:

    # Constructor

    def __init__(self, pieces, rank, period, increment):
        if pieces[-1].x_end == rank:
            self.transient_pieces = pieces
            self.periodic_pieces = []
        else:
            self.transient_pieces, self.periodic_pieces = self.split_pieces(pieces, rank, period)
        self.rank = Fraction(rank)
        self.period = Fraction(period)
        if increment != math.inf and increment != -math.inf:
            self.increment = Fraction(increment)
        else:
            self.increment = increment
        self.periodic_slope = self.increment / self.period
        self.all_pieces = self.transient_pieces + self.periodic_pieces

    @staticmethod
    def from_elements(elements, rank, period, increment):
        pieces = []
        spot = None
        segment = None
        for e in elements:
            if e.is_spot:
                spot = e
            if e.is_segment:
                segment = e
            if (spot is not None) and (segment is not None):
                piece = Piece(spot.x_start, spot.y, segment.y_segment, segment.x_end, segment.slope)
                pieces.append(piece)
                spot = None
                segment = None
        return PiecewiseLinearFunction(pieces, rank, period, increment)

    # Transformation methods

    # Extends the periodic part up to the target_x
    def extend(self, target_x: Fraction):
        if len(self.periodic_pieces) == 0:
            return self

        period = target_x - self.rank
        increment = period / self.period * self.increment

        if self.is_ultimately_affine():
            e = self.periodic_pieces[0]
            extended_piece = Piece(e.x_start, e.y_spot, e.y_segment, target_x, e.slope)
            return PiecewiseLinearFunction(self.transient_pieces + [extended_piece], self.rank, period, increment)

        no_of_repeated_periods = math.ceil((target_x - (self.rank + self.period)) / self.period)
        result_pieces = self.transient_pieces + self.periodic_pieces
        for i in range(no_of_repeated_periods):
            for e in self.periodic_pieces:
                result_pieces.append(Piece(e.x_start + self.period * (i + 1), e.y_spot + self.increment * (i + 1),
                                           e.y_segment + self.increment * (i + 1), e.x_end + self.period * (i + 1),
                                           e.slope))
        return PiecewiseLinearFunction(result_pieces, self.rank, period, increment)

    def decompose(self):
        decomposed_transient = []
        for e in self.transient_pieces:
            spot, segment = e.decompose()
            decomposed_transient.append(spot)
            decomposed_transient.append(segment)
        decomposed_periodic = []
        for e in self.periodic_pieces:
            spot, segment = e.decompose()
            decomposed_periodic.append(spot)
            decomposed_periodic.append(segment)
        return decomposed_transient, decomposed_periodic

    # Splits the pieces into transient and periodic parts at rank T,
    # and cuts off pieces defined on x > T + d
    def split_pieces(self, pieces, rank, period):
        split_index = Piece.index_of_piece_at(pieces, rank)
        split_el = pieces[split_index]
        if split_el.x_start == rank:
            transient_pieces = pieces[0:split_index]
            periodic_pieces = self.cut_off(pieces[split_index:], rank + period)
        else:
            left_piece = Piece(split_el.x_start, split_el.y_spot, split_el.y_segment, rank, split_el.slope)
            right_piece = Piece(rank, split_el.value_at(rank), split_el.value_at(rank), split_el.x_end,
                                split_el.slope)
            transient_pieces = pieces[0:split_index] + [left_piece]
            periodic_pieces = self.cut_off([right_piece] + pieces[split_index + 1:], rank + period)
        return transient_pieces, periodic_pieces

    def cut_off(self, pieces, end_x):
        last_index = Piece.index_of_piece_at(pieces, end_x)
        if last_index is None:
            last_index = len(pieces) - 1
        last_piece = pieces[last_index]
        if last_piece.x_start == end_x:
            return pieces[0:last_index]
        else:
            last_piece_cut = Piece(last_piece.x_start, last_piece.y_spot, last_piece.y_segment, end_x,
                                   last_piece.slope)
            return pieces[0:last_index] + [last_piece_cut]

    # Shifts the function up by y
    # Relevant for concave convolution
    def shift_vertically(self, y):
        result_pieces = []
        for p in self.all_pieces:
            shifted_piece = Piece(p.x_start, p.y_spot + y, p.y_segment + y, p.x_end, p.slope)
            result_pieces.append(shifted_piece)
        return PiecewiseLinearFunction(result_pieces, self.rank, self.period, self.increment)

    # Calculation methods

    def value_at(self, x):
        if x < self.rank:
            i = Piece.index_of_piece_at(self.transient_pieces, x)
            if x == self.transient_pieces[i].x_start:
                return self.transient_pieces[i].y_spot
            else:
                return self.transient_pieces[i].value_at(x)
        else:
            if self.is_ultimately_affine():
                e = self.periodic_pieces[0]
                return (x - e.x_start) * e.slope + e.y_segment
            no_of_periods = math.floor((x - (self.rank + self.period)) / self.period + 1)
            if no_of_periods < 0:
                no_of_periods = 0
            total_increment = no_of_periods * self.increment
            defined_value_at = x - no_of_periods * self.period

            i = Piece.index_of_piece_at(self.periodic_pieces, defined_value_at)
            p = self.periodic_pieces[i]
            return p.value_at(defined_value_at) + total_increment

    # Computes the supremum of deviations from the average slope of the periodic part
    def sup_deviation_from_periodic_slope(self):
        sup = -math.inf
        for e in self.periodic_pieces:
            sup = max(sup, e.y_spot - self.periodic_slope * e.x_start)
            sup = max(sup, e.y_segment - self.periodic_slope * e.x_start)
            sup = max(sup, e.lim_value_at(e.x_end) - self.periodic_slope * e.x_end)
        return sup

    # Computes the infimum of deviations from the average slope of the periodic part
    def inf_deviation_from_periodic_slope(self):
        inf = float("inf")
        for e in self.periodic_pieces:
            inf = min(inf, e.y_spot - self.periodic_slope * e.x_start)
            inf = min(inf, e.y_segment - self.periodic_slope * e.x_start)
            inf = min(inf, e.lim_value_at(e.x_end) - self.periodic_slope * e.x_end)
        return inf

    def is_ultimately_affine(self):
        no_discontinuities = self.periodic_pieces[0].y_segment + self.increment == self.periodic_pieces[0].lim_value_at(self.periodic_pieces[0].x_end)
        return len(self.periodic_pieces) == 1 and no_discontinuities

    def is_convex(self):
        current_piece = self.all_pieces[0]
        if current_piece.y_spot < current_piece.y_segment:
            return False
        if not self.is_ultimately_affine():
            return False
        for p in self.all_pieces[1:]:
            if p.slope < current_piece.slope:
                return False
            if current_piece.lim_value_at(p.x_start) != p.y_spot:
                return False
            if p.y_spot != p.y_segment:
                return False
            current_piece = p
        return True

    def is_concave(self):
        current_piece = self.all_pieces[0]
        if current_piece.y_spot > current_piece.y_segment:
            return False
        if not self.is_ultimately_affine():
            return False
        for p in self.all_pieces[1:]:
            if p.slope > current_piece.slope:
                return False
            if current_piece.lim_value_at(p.x_start) != p.y_spot:
                return False
            if p.y_spot != p.y_segment:
                return False
            current_piece = p
        return True

    def __str__(self):
        ret_str = "{rank: " + str(self.rank) + ", period: " + str(self.period) + ", increment: " + str(
            self.increment) + "\n" + "TransEl:\n"
        for e in self.transient_pieces:
            ret_str = ret_str + str(e) + "\n"
        ret_str = ret_str + "PerEl:\n"
        for e in self.periodic_pieces:
            ret_str = ret_str + str(e) + "\n"
        return ret_str

    def __eq__(self, other):
        if not isinstance(other, PiecewiseLinearFunction):
            return False
        if len(self.all_pieces) != len(other.all_pieces):
            return False
        for i in range(len(self.all_pieces)):
            if self.all_pieces[i] != other.all_pieces[i]:
                return False
        return self.rank == other.rank and self.period == other.period and self.increment == other.increment


    #TODO Remove
    def gg(self):
        def fract(f):
            return "new Rational({},{})".format(f.numerator, f.denominator)

        result_string = "new Curve( \n baseSequence: new Sequence(new Element[] \n { \n"

        for p in self.all_pieces:
            result_string = result_string + "new Point( {},{} ), \n".format(fract(p.x_start), fract(p.y_spot))
            result_string = result_string + "new Segment( {}, {}, {}, {} ), \n".format(fract(p.x_start), fract(p.x_end), fract(p.y_segment), fract(p.slope))
        result_string = result_string + "}"
        result_string = result_string + "), \n pseudoPeriodStart: {} , \n pseudoPeriodLength: {}".format(fract(self.rank), fract(self.period))
        result_string = result_string + ", \n pseudoPeriodHeight: {}\n);".format(fract(self.increment))
        return result_string