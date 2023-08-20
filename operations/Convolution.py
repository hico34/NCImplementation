from helpers.util import lcm_fraction as lcm
from model.PiecewiseLinearFunction import PiecewiseLinearFunction
from model.Element import Element
from model.Spot import Spot
from model.Segment import Segment
from operations.Minimum import min_of_unsorted_elements, min_of_elements, min_of_plfs


def convolution(f1: PiecewiseLinearFunction, f2: PiecewiseLinearFunction):
    period = lcm(f1.period, f2.period)
    increment = period * min(f1.periodic_slope, f2.periodic_slope)
    g1 = transient_convolution(f1, f2)
    g2 = transient_periodic_convolution(f1, f2)
    g3 = transient_periodic_convolution(f2, f1)
    g4 = periodic_convolution(f1, f2, period, increment)
    g12 = min_of_plfs(g1, g2)
    g123 = min_of_plfs(g12, g3)
    g = min_of_plfs(g123, g4)
    return g


# Convolution of transient parts of two functions
def transient_convolution(f1: PiecewiseLinearFunction, f2: PiecewiseLinearFunction):
    decomposed_f1, _ = f1.decompose()
    decomposed_f2, _ = f2.decompose()
    convolutions = []
    for e1 in decomposed_f1:
        for e2 in decomposed_f2:
            convolutions = convolutions + element_convolution(e1, e2)
    lower_envelope = min_of_unsorted_elements(convolutions)
    return PiecewiseLinearFunction.from_elements(lower_envelope, None, None, None)


# Convolution of periodic parts of two functions
def periodic_convolution(f1: PiecewiseLinearFunction, f2: PiecewiseLinearFunction, period, increment):
    _, f1_elements = f1.extend(f1.rank + f1.rank + 2 * period).decompose()
    _, f2_elements = f2.extend(f2.rank + f2.rank + 2 * period).decompose()

    convolutions = []
    for e1 in f1_elements:
        for e2 in f2_elements:
            convolutions = convolutions + element_convolution(e1, e2)

    lower_envelope = min_of_unsorted_elements(convolutions)

    return PiecewiseLinearFunction.from_elements(lower_envelope, f1.rank + f2.rank + period, period, increment)


# Convolution of transient part of one, and periodic part of another function
def transient_periodic_convolution(f_transient: PiecewiseLinearFunction, f_periodic: PiecewiseLinearFunction):
    _, decomposed_f_periodic = f_periodic.extend(f_periodic.rank + f_transient.rank + f_periodic.period).decompose()
    decomposed_f_transient, _ = f_transient.decompose()

    convolutions = []
    for e1 in decomposed_f_transient:
        for e2 in decomposed_f_periodic:
            convolutions = convolutions + element_convolution(e1, e2)

    lower_envelope = min_of_unsorted_elements(convolutions)

    return PiecewiseLinearFunction.from_elements(lower_envelope, f_transient.rank + f_periodic.rank, f_periodic.period, f_periodic.increment)


def element_convolution(e1: Element, e2: Element):
    if isinstance(e1, Spot):
        if isinstance(e2, Spot):
            return [[spot_convolution(e1, e2)]]
        else:
            return [[spot_segment_convolution(e1, e2)]]
    else:
        if isinstance(e2, Spot):
            return [[spot_segment_convolution(e2, e1)]]
        else:
            s1, s2, s3 = segment_convolution(e1, e2)
            return [[s1], [s2], [s3]]


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
    x_split = lower.x_end + upper.x_start
    y_split = lower.lim_value_at(lower.x_end) + upper.y_segment
    x_end = lower.x_end + upper.x_end
    left_segment = Segment(x_start, y_split, x_split, lower.slope)
    spot = Spot(x_split, y_split)
    right_segment = Segment(x_split, y_split, x_end, upper.slope)
    return left_segment, spot, right_segment
