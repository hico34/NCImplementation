from heapq import merge
from helpers.util import lcm_fraction as lcm
from collections import OrderedDict
from helpers.plfHelper import index_of_piece_at
from model.Piece import Piece
from model.PiecewiseLinearFunction import PiecewiseLinearFunction

def add_plfs(f1: PiecewiseLinearFunction, f2: PiecewiseLinearFunction):
    if f1.rank > f2.rank:
        rank = f1.rank
    else:
        rank = f2.rank
    period = lcm(f1.period, f2.period)
    increment = (f1.increment / f1.period + f2.increment / f2.period) * period

    f1_extended_pieces = f1.extend(rank + period).all_pieces
    f2_extended_pieces = f2.extend(rank + period).all_pieces
    f1_extended_spots = list(map(lambda el: el.x_start, f1_extended_pieces))
    f2_extended_spots = list(map(lambda el: el.x_start, f2_extended_pieces))
    merged_spots = list(OrderedDict.fromkeys(merge(f1_extended_spots, f2_extended_spots))) ##TODO own merge
    result_pieces = []
    for i in range(len(merged_spots)):
        if i == len(merged_spots) - 1:
            x_end = rank + period
        else:
            x_end = merged_spots[i + 1]
        x_start = merged_spots[i]
        y_spot = f1.value_at(x_start) + f2.value_at(x_start)
        f1_piece = f1_extended_pieces[index_of_piece_at(f1_extended_pieces, x_start)]
        f2_piece = f2_extended_pieces[index_of_piece_at(f2_extended_pieces, x_start)]
        y_segment = f1_piece.lim_value_at(x_start) + f2_piece.lim_value_at(x_start)
        slope = f1_piece.slope + f2_piece.slope

        result_pieces.append(Piece(x_start, y_spot, y_segment, x_end, slope))
    return PiecewiseLinearFunction(result_pieces, rank, period, increment)

def subtract_plfs(f1: PiecewiseLinearFunction, f2: PiecewiseLinearFunction):
    if f1.rank > f2.rank:
        rank = f1.rank
    else:
        rank = f2.rank
    period = lcm(f1.period, f2.period)
    increment = (f1.increment / f1.period - f2.increment / f2.period) * period
    f1_extended_pieces = f1.extend_and_get_all_pieces(rank, period)
    f2_extended_pieces = f2.extend_and_get_all_pieces(rank, period)
    f1_extended_spots = list(map(lambda el: el.x_start, f1_extended_pieces))
    f2_extended_spots = list(map(lambda el: el.x_start, f2_extended_pieces))
    merged_spots = list(OrderedDict.fromkeys(merge(f1_extended_spots, f2_extended_spots)))
    result_pieces = []
    for i in range(len(merged_spots)):
        x_start = merged_spots[i]
        y_spot = f1.value_at(x_start) - f2.value_at(x_start)
        f1_piece = f1_extended_pieces[index_of_piece_at(f1_extended_pieces, x_start)]
        f2_piece = f2_extended_pieces[index_of_piece_at(f2_extended_pieces, x_start)]
        y_segment = f1_piece.y_segment - f2_piece.y_segment
        slope = f1_piece.slope - f2_piece.slope
        if i == len(merged_spots) - 1:
            x_end = rank + period
        else:
            x_end = merged_spots[i+1]
        result_pieces.append(Piece(x_start, y_spot, y_segment, x_end, slope))
    return PiecewiseLinearFunction(result_pieces, rank, period, increment)


