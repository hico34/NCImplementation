from model.Piece import Piece
from helpers.util import lcm_fraction as lcm
from model.PiecewiseLinearFunction import PiecewiseLinearFunction
from fractions import Fraction


def min_of_plfs(f1, f2):
    #Precompute rank
    if f1.periodic_slope < f2.periodic_slope:
        period = f1.period
        increment = f1.increment
        M1 = f1.sup_deviation_from_periodic_slope()
        m2 = f2.inf_deviation_from_periodic_slope()
        rank = max((M1-m2)/(f2.periodic_slope - f1.periodic_slope), f1.rank, f2.rank)
    elif f2.periodic_slope < f1.periodic_slope:
        period = f2.period
        increment = f2.increment
        M1 = f2.sup_deviation_from_periodic_slope()
        m2 = f1.inf_deviation_from_periodic_slope()
        rank = max((M1-m2)/(f1.periodic_slope - f2.periodic_slope), f1.rank, f2.rank)
    else:
        period = lcm(f1.period, f2.period)
        increment = lcm(f1.increment, f2.increment) * f1.periodic_slope
        rank = max(f1.rank, f2.rank)
    f1_pieces = f1.extend_and_get_all_pieces(rank, period)
    f2_pieces = f2.extend_and_get_all_pieces(rank, period)

    result_pieces = []
    i = 0
    j = 0
    current_spot_x = 0
    while i < len(f1_pieces) and j < len(f2_pieces):
        f1_piece = f1_pieces[i]
        f2_piece = f2_pieces[j]
        y_spot = min(f1_piece.value_at(current_spot_x), f2_piece.value_at(current_spot_x))
        next_spot_x = min(f1_piece.x_end, f2_piece.x_end)
        if f1_piece.slope != f2_piece.slope:
            #TODO Prove Correctnes
            intersection_x = (f2_piece.y_segment - f2_piece.slope * f2_piece.x_start - f1_piece.y_segment + f1_piece.slope*f1_piece.x_start) / (f1_piece.slope - f2_piece.slope)

        else:
            intersection_x = -1
        if current_spot_x < intersection_x < next_spot_x:
            # Lower piece refers to the piece with the lower limit at current_spot_x.
            # Min(f1, f2) in the currently analysed interval will then be lower_piece up to the intersection,
            # and upper_piece after
            if f1_piece.lim_value_at(current_spot_x) < f2_piece.lim_value_at(current_spot_x):
                lower_piece = f1_piece
                upper_piece = f2_piece
            else:
                lower_piece = f2_piece
                upper_piece = f1_piece
            result_pieces.append(Piece(current_spot_x, y_spot, lower_piece.lim_value_at(current_spot_x), intersection_x, lower_piece.slope))
            intersection_y = f1_piece.value_at(intersection_x)
            result_pieces.append(
                Piece(intersection_x, intersection_y, intersection_y, next_spot_x, upper_piece.slope))
        elif f1_piece.lim_value_at(current_spot_x) < f2_piece.lim_value_at(current_spot_x) or (f1_piece.lim_value_at(current_spot_x) == f2_piece.lim_value_at(current_spot_x) and f1_piece.slope < f2_piece.slope):
            # TODO Avoid unnecessary pieces
            result_pieces.append(
                Piece(current_spot_x, y_spot, f1_piece.lim_value_at(current_spot_x), next_spot_x, f1_piece.slope))
        else:
            result_pieces.append(
                Piece(current_spot_x, y_spot, f2_piece.lim_value_at(current_spot_x), next_spot_x, f2_piece.slope))

        if f1_piece.x_end < f2_piece.x_end:
            i = i + 1
        elif f2_piece.x_end < f1_piece.x_end:
            j = j + 1
        else:
            i = i + 1
            j = j + 1
        current_spot_x = next_spot_x
    return PiecewiseLinearFunction(result_pieces, rank, period, increment)
