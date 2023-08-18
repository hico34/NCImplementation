from helpers.plfHelper import index_of_piece_at
import math
from .Piece import Piece


class PiecewiseLinearFunction:
    def __init__(self, pieces, rank, period, increment):
        if not (rank is None):
            self.transient_pieces, self.periodic_pieces = self.split_pieces(pieces, rank, period)
        else:
            self.transient_pieces = pieces
        self.all_pieces = pieces
        self.rank = rank
        self.period = period
        self.increment = increment
        self.periodic_slope = increment / period

    def value_at(self, x):
        if x < self.rank:
            i = index_of_piece_at(self.transient_pieces, x)
            if x == self.transient_pieces[i].x_start:
                return self.transient_pieces[i].y_spot
            else:
                return self.transient_pieces[i].y_segment + (x - self.transient_pieces[i].x_start) * \
                       self.transient_pieces[i].slope
        else:
            if self.is_ultimately_affine():
                e = self.periodic_pieces[0]
                return (x - e.x_start) * e.slope + e.y_segment
            no_of_periods = math.floor((x - (self.rank + self.period)) / self.period + 1)
            if no_of_periods < 0:
                no_of_periods = 0
            total_increment = no_of_periods * self.increment
            defined_value_at = x - no_of_periods * self.period

            i = index_of_piece_at(self.periodic_pieces, defined_value_at)
            if defined_value_at == self.periodic_pieces[i].x_start:
                value = self.periodic_pieces[i].y_spot
            else:
                value = self.periodic_pieces[i].y_segment + (defined_value_at - self.periodic_pieces[i].x_start) * \
                        self.periodic_pieces[i].slope
            return value + total_increment

    #TODO Replace Usages
    def extend_and_get_all_pieces(self, rank, period):
        if rank < self.rank or period % self.period != 0:
            print("Error at extend?")  # TODO
        if self.is_ultimately_affine():
            e = self.periodic_pieces[0]
            extended_piece = Piece(e.x_start, e.y_spot, e.y_segment, rank + period, e.slope)
            return self.transient_pieces + [extended_piece]
        no_of_repeated_periods = math.ceil((rank + period - (self.rank + self.period)) / self.period)
        result_pieces = self.transient_pieces + self.periodic_pieces
        for i in range(no_of_repeated_periods):
            for e in self.periodic_pieces:
                result_pieces.append(Piece(e.x_start + self.period * (i + 1), e.y_spot + self.increment * (i + 1),
                                             e.y_segment + self.increment * (i + 1), e.x_end + self.period * (i + 1),
                                             e.slope))
        return self.cut_off(result_pieces, rank + period)

    # Computes the supremum of deviations from the average slope of the periodic part (increment/period)
    def sup_deviation_from_periodic_slope(self):
        sup = 0
        for e in self.periodic_pieces:
            sup = max(sup, e.y_spot - self.periodic_slope * e.x_start) #TODO Correct?
            sup = max(sup, e.y_segment - self.periodic_slope * e.x_start)
            sup = max(sup, (e.y_segment + e.slope * e.x_end) - self.periodic_slope * e.x_end)
        return sup

    # Computes the infimum of deviations from the average slope of the periodic part (increment/period)
    def inf_deviation_from_periodic_slope(self):
        inf = float("inf")
        for e in self.periodic_pieces:
            inf = min(inf, e.y_spot - self.periodic_slope * e.x_start)
            inf = min(inf, e.y_segment - self.periodic_slope * e.x_start)
            inf = min(inf, (e.y_segment + e.slope * e.x_end) - self.periodic_slope * e.x_end)
        return inf

    def __str__(self):
        retStr = "{rank: " + str(self.rank) + ", period: " + str(self.period) + ", increment: " + str(
            self.increment) + "\n" + "TransEl:\n"
        for e in self.transient_pieces:
            retStr = retStr + str(e) + "\n"
        retStr = retStr + "PerEl:\n"
        for e in self.periodic_pieces:
            retStr = retStr + str(e) + "\n"
        return retStr

    # Splits the pieces into transient and periodic parts at rank T,
    # and cuts off pieces defined on x > T + d
    def split_pieces(self, pieces, rank, period):
        split_index = index_of_piece_at(pieces, rank)
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
        last_index = index_of_piece_at(pieces, end_x)
        if last_index is None:
            last_index = len(pieces) - 1
        last_piece = pieces[last_index]
        if last_piece.x_start == end_x:
            return pieces[0:last_index]
        else:
            last_piece_cut = Piece(last_piece.x_start, last_piece.y_spot, last_piece.y_segment, end_x,
                                     last_piece.slope)
            return pieces[0:last_index] + [last_piece_cut]

    def is_ultimately_affine(self):
        return len(self.periodic_pieces) == 1

    def numpy_values_at(self, np_array):
        import numpy as np
        pieces = self.extend_and_get_all_pieces(np_array[np_array.size - 1] + self.period, 0)
        condlist = []
        funclist = []
        x = np_array
        for e in pieces:
            condlist.append(x == e.x_start)
            funclist.append(e.y_spot)
            condlist.append(np.logical_and((e.x_start < x),(x < e.x_end)))
            funclist.append(lambda x, e=e: e.numpy_value_at(x))

        return np.piecewise(x, condlist, funclist)
