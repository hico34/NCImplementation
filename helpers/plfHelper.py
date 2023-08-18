import random
from fractions import Fraction
from model.Piece import Piece
#from PiecewiseLinearFunction import PiecewiseLinearFunction

def index_of_piece_at(pieces: [Piece], x):
    # TODO Binary Search
    for i in range(len(pieces)):
        if pieces[i].x_start <= x < pieces[i].x_end:
            return i
    return None


# def generate_plf(no_of_elements, max_interval_size, max_slope_size, max_y_segment_size, continous):
#     random.seed(14334)
#     elements = []
#     next_x_start = Fraction(0)
#     next_y_segment = Fraction(0)
#     no_of_period_segments = random.randint(0, 20)
#     for i in range(no_of_elements):
#         if continous:
#             y_segment = next_y_segment
#             y_spot = next_y_segment
#         else:
#             y_segment = randomFraction(0, max_y_segment_size)
#             y_spot = randomFraction(0, 1000)
#         x_end = randomFraction(1, max_interval_size)
#         slope = randomFraction(0, max_slope_size)
#         elements.append(Element(next_x_start, y_spot, y_segment, x_end, slope))
#         next_y_segment = y_segment + x_end * slope #TODO Wrong
#         next_x_start = x_end
#
#     rank = elements[-no_of_period_segments].x_start
#     period = elements[len(elements)-1].x_end - rank
#     increment = (elements[len(elements)-1].y_segment + elements[len(elements)-1].slope * elements[len(elements)-1].x_end) - elements[-no_of_period_segments].y_spot
#     return PiecewiseLinearFunction(elements, rank, period, increment)

def merge_piece_lists(l1, l2):
    mergedList = []

def randomFraction(a, b):
    den = random.randint(0, 1000)
    num = random.randint(a * den, b * den)
    return Fraction(num, den)