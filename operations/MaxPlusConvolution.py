from util.util import lcm_fraction as lcm
from model.PiecewiseLinearFunction import PiecewiseLinearFunction
from model.Element import Element
from model.Spot import Spot
from model.Segment import Segment
from operations.Maximum import max_of_unsorted_elements, maximum
import math
from model.Piece import Piece


def maxplus_convolution(f1: PiecewiseLinearFunction, f2: PiecewiseLinearFunction):
    if f1.is_concave() and f2.is_concave():
        return maxplus_concave_convolution(f1, f2)
    if f1.is_convex() and f2.is_convex():
        return maxplus_convex_convolution(f1, f2)
    period = lcm(f1.period, f2.period)
    increment = period * max(f1.periodic_slope, f2.periodic_slope)
    g1 = maxplus_transient_convolution(f1, f2)
    g2 = maxplus_transient_periodic_convolution(f1, f2)
    g3 = maxplus_transient_periodic_convolution(f2, f1)
    g4 = maxplus_periodic_convolution(f1, f2, period, increment)
    g12 = maximum(g1, g2)
    g123 = maximum(g12, g3)
    g = maximum(g123, g4)
    return g


# Convolution of two convex functions
def maxplus_concave_convolution(f1: PiecewiseLinearFunction, f2: PiecewiseLinearFunction):
    iter1 = iter(f1.all_pieces)
    iter2 = iter(f2.all_pieces)

    current_p1 = next(iter1, None)
    current_p2 = next(iter2, None)
    next_y = f1.all_pieces[0].lim_value_at(0) + f2.all_pieces[0].lim_value_at(0)
    next_x = 0
    result_pieces = []
    while current_p1 is not None and current_p2 is not None:
        # If infinite piece is encountered, discard all pieces with smaller slopes
        if current_p1.x_start == f1.rank and current_p1.slope > current_p2.slope:
            p = Piece(next_x, next_y, next_y, next_x + 1, current_p1.slope)
            result_pieces.append(p)
            rank = next_x
            period = 1
            increment = p.slope
            break
        elif current_p2.x_start == f2.rank and current_p1.slope < current_p2.slope:
            p = Piece(next_x, next_y, next_y, next_x + 1, current_p2.slope)
            result_pieces.append(p)
            rank = next_x
            period = 1
            increment = p.slope
            break

        # Concatenate piece with steper slope
        if current_p2 is None or current_p1.slope > current_p2.slope:
            p = Piece(next_x, next_y, next_y, next_x + current_p1.x_end - current_p1.x_start, current_p1.slope)
            result_pieces.append(p)

            next_x = next_x + current_p1.x_end - current_p1.x_start
            next_y = p.lim_value_at(next_x)
            current_p1 = next(iter1, None)
        elif current_p1 is None or current_p1.slope < current_p2.slope:
            p = Piece(next_x, next_y, next_y, next_x + current_p2.x_end - current_p2.x_start, current_p2.slope)
            result_pieces.append(p)

            next_x = next_x + current_p2.x_end - current_p2.x_start
            next_y = p.lim_value_at(next_x)
            current_p2 = next(iter2, None)
        elif current_p1.slope == current_p2.slope:
            # Avoid unnecessary pieces if slopes are equal
            p = Piece(next_x, next_y, next_y, next_x + current_p1.x_end - current_p1.x_start + current_p2.x_end - current_p2.x_start, current_p2.slope)
            result_pieces.append(p)
            next_x = next_x + current_p1.x_end - current_p1.x_start + current_p2.x_end - current_p2.x_start
            next_y = p.lim_value_at(next_x)
            current_p1 = next(iter1, None)
            current_p2 = next(iter2, None)

    # Fix convolution at potential discontinuity at x = 0
    result_pieces[0].y_spot = f1.value_at(0) + f2.value_at(0)
    return PiecewiseLinearFunction(result_pieces, rank, period, increment)


# Convolution of two concave functions
def maxplus_convex_convolution(f1: PiecewiseLinearFunction, f2: PiecewiseLinearFunction):
    f1_zero = f1.all_pieces[0].y_spot
    f2_zero = f2.all_pieces[0].y_spot
    if f1_zero == 0 == f2_zero:
        return maximum(f1, f2)
    f1_shifted = f1.shift_vertically(-f1_zero)
    f2_shifted = f2.shift_vertically(-f2_zero)
    g_shifted = maximum(f1_shifted, f2_shifted)
    g = g_shifted.shift_vertically(+f1_zero + f2_zero)
    return g


# Convolution of transient parts of two functions
def maxplus_transient_convolution(f1: PiecewiseLinearFunction, f2: PiecewiseLinearFunction):
    decomposed_f1, _ = f1.decompose()
    decomposed_f2, _ = f2.decompose()
    convolutions = []
    for e1 in decomposed_f1:
        for e2 in decomposed_f2:
            convolutions = convolutions + maxplus_element_convolution(e1, e2)

    upper_envelope = max_of_unsorted_elements(convolutions)
    return PiecewiseLinearFunction.from_elements(upper_envelope, upper_envelope[-1].x_end, 1, -math.inf)


# Convolution of periodic parts of two functions
def maxplus_periodic_convolution(f1: PiecewiseLinearFunction, f2: PiecewiseLinearFunction, period, increment):
    _, f1_elements = f1.extend(f1.rank + f1.rank + 2 * period).decompose()
    _, f2_elements = f2.extend(f2.rank + f2.rank + 2 * period).decompose()

    definition_end = f1.rank + f2.rank + 2*period
    convolutions = []
    for e1 in f1_elements:
        for e2 in f2_elements:
            # We can disregard values outside of the needed definition range
            if (e1.x_start + e2.x_start) < definition_end:
                convolutions = convolutions + maxplus_element_convolution(e1, e2)

    upper_envelope = max_of_unsorted_elements(convolutions)

    return PiecewiseLinearFunction.from_elements(upper_envelope, f1.rank + f2.rank + period, period, increment)


# Convolution of transient part of one, and periodic part of another function
def maxplus_transient_periodic_convolution(f_transient: PiecewiseLinearFunction, f_periodic: PiecewiseLinearFunction):
    _, decomposed_f_periodic = f_periodic.extend(f_periodic.rank + f_transient.rank + f_periodic.period).decompose()
    decomposed_f_transient, _ = f_transient.decompose()

    convolutions = []
    for e1 in decomposed_f_transient:
        for e2 in decomposed_f_periodic:
            convolutions = convolutions + maxplus_element_convolution(e1, e2)

    upper_envelope = max_of_unsorted_elements(convolutions)

    return PiecewiseLinearFunction.from_elements(upper_envelope, f_transient.rank + f_periodic.rank, f_periodic.period, f_periodic.increment)


def maxplus_element_convolution(e1: Element, e2: Element):
    if isinstance(e1, Spot):
        if isinstance(e2, Spot):
            return [[spot_convolution(e1, e2)]]
        else:
            return [[spot_segment_convolution(e1, e2)]]
    else:
        if isinstance(e2, Spot):
            return [[spot_segment_convolution(e2, e1)]]
        else:
            s1, s2, s3 = maxplus_segment_convolution(e1, e2)
            return [[s1], [s2], [s3]]


def spot_convolution(s1: Spot, s2: Spot):
    return Spot(s1.x_start + s2.x_start, s1.y + s2.y)


def spot_segment_convolution(spot: Spot, segment: Segment):
    return Segment(segment.x_start + spot.x_start, segment.y_segment + spot.y, segment.x_end + spot.x_start, segment.slope)


def maxplus_segment_convolution(s1: Segment, s2: Segment):
    if s1.slope < s2.slope:
        lower = s1
        upper = s2
    else:
        lower = s2
        upper = s1
    x_start = lower.x_start + upper.x_start
    x_split = upper.x_end + lower.x_start
    y_split = upper.lim_value_at(upper.x_end) + lower.y_segment
    x_end = lower.x_end + upper.x_end
    left_segment = Segment(x_start, upper.y_segment + lower.y_segment, x_split, upper.slope)
    spot = Spot(x_split, y_split)
    right_segment = Segment(x_split, y_split, x_end, lower.slope)
    return left_segment, spot, right_segment