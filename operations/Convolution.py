from helpers.util import lcm_fraction as lcm
from helpers.util import decompose
from model.PiecewiseLinearFunction import PiecewiseLinearFunction
from model.Piece import Piece
from model.Spot import Spot
from model.Segment import Segment


def convolution(f1: PiecewiseLinearFunction, f2: PiecewiseLinearFunction):
    period = lcm(f1.period, f2.period)
    increment = period * min(f1.periodic_slope, f2.periodic_slope)
    g1 = transient_convolution(f1.transient_pieces, f2.transient_pieces)
    g2 = transient_periodic_convolution(f1, f2)
    g3 = transient_periodic_convolution(f2, f1)
    g4 = periodic_convolution(f1, f2, period)


def transient_convolution(f1_pieces: [Piece], f2_pieces: [Piece]):
    decomposed_f1 = decompose(f1_pieces)
    decomposed_f2 = decompose(f2_pieces)
    convolutions = []
    for e1 in decomposed_f1:
        for e2 in decomposed_f2:
            convolutions = convolutions + element_convolution(e1, e2)
    return convolutions

def periodic_convolution(f1, f2, period):
    periodic_index = len(f1.transient_pieces)
    f_periodic_extended = f1.extend_and_get_all_pieces(f1.rank, f1.rank + 2 * period)
    f1_periodic_pieces = f_periodic_extended[periodic_index:]
    periodic_index = len(f2.transient_pieces)
    f_periodic_extended = f2.extend_and_get_all_pieces(f2.rank, f2.rank + 2 * period)
    f2_periodic_pieces = f_periodic_extended[periodic_index:]
    decomposed_f1 = decompose(f1_periodic_pieces)
    decomposed_f2 = decompose(f2_periodic_pieces)
    convolutions = []
    for e1 in decomposed_f1:
        for e2 in decomposed_f2:
            convolutions = convolutions + element_convolution(e1, e2)
    return convolutions

def transient_periodic_convolution(f_transient, f_periodic):
    periodic_index = len(f_transient.transient_pieces)
    f_periodic_extended = f_transient.extend_and_get_all_pieces(f_transient.rank, f_transient.rank + f_periodic.rank + f_transient.period)
    f_periodic_pieces = f_periodic_extended[periodic_index:]
    decomposed_f1 = decompose(f_transient.transient_pieces)
    decomposed_f2 = decompose(f_periodic_pieces)
    convolutions = []
    for e1 in decomposed_f1:
        for e2 in decomposed_f2:
            convolutions = convolutions + element_convolution(e1, e2)
    return convolutions

def element_convolution(e1, e2):
    if isinstance(e1, Spot):
        if isinstance(e2, Spot):
            return [spot_convolution(e1, e2)]
        else:
            return [spot_segment_convolution(e1, e2)]
    else:
        if isinstance(e2, Spot):
            return [spot_segment_convolution(e2, e1)]
        else:
            s1, s2 = segment_convolution(e1, e2)
            return [s1, s2]

def spot_convolution(s1: Spot, s2: Spot):
    return Spot(s1.x_start + s2.x_start, s1.y + s2.y)

def spot_segment_convolution(spot: Spot, segment: Segment):
    return Segment(segment.x_start + spot.x_start, segment.y_segment + spot.y, segment.x_end + spot.x_start, segment.slope)

def segment_convolution(s1: Segment, s2: Segment):
    if s1.slope < s2.slope:
        lower = s1
        upper = s2
    else:
        lower = s2
        upper = s1
    x_start = lower.x_start + upper.x_start
    y_segment_1 = lower.y_segment + upper.y_segment - lower.slope * lower.x_start - lower.slope * upper.x_start
    x_split = lower.x_end + upper.x_start
    x_end = lower.x_end + upper.x_end
    return_segment_1 = Segment(x_start, y_segment_1, x_split, lower.slope)
    y_segment_2 = lower.y_segment + upper.y_segment + lower.slope * (lower.x_end - lower.x_start) - upper.slope * lower.x_end - upper.slope * upper.x_start
    return_segment_2 = Segment(x_split, y_segment_2, x_end, upper.slope)
    return return_segment_1, return_segment_2

def min_of_elements(elements: list):
    elements.sort(key=lambda e: e.x_start)
    element_collections = []
    current_bag_x = elements[0].x_start
    for e in elements:
        print()