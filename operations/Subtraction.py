from util.util import lcm_fraction as lcm
from model.PiecewiseLinearFunction import PiecewiseLinearFunction
from model.Element import Element
from util.util import append
from model.Spot import Spot
from model.Segment import Segment

def subtract_functions(f1: PiecewiseLinearFunction, f2: PiecewiseLinearFunction):
    rank = max(f1.rank, f2.rank)
    period = lcm(f1.period, f2.period)
    increment = (f1.increment / f1.period - f2.increment / f2.period) * period

    t, p = f1.extend(rank + period).decompose()
    f1_elements = t + p
    t, p = f2.extend(rank + period).decompose()
    f2_elements = t + p

    result_elements = subtract_elements(f1_elements, f2_elements)

    return PiecewiseLinearFunction.from_elements(result_elements, rank, period, increment)

# Requires lists sorted by x_start, and spots < segments if both start at the same value
# Elements in the same list may not overlap
# Elements must be defined from x = 0 to x_end of the last element, but one list may have a later end
def subtract_elements(e1: [Element], e2: [Element]):
    result = []
    iter1 = iter(e1)
    iter2 = iter(e2)

    current_e1: Element = next(iter1, None)
    current_e2: Element = next(iter2, None)

    leftover_e1 = None
    leftover_e2 = None

    # Cheats leftover values into the iterator
    def next_e1():
        nonlocal leftover_e1
        if leftover_e1 is not None:
            next_val = leftover_e1
            leftover_e1 = None
            return next_val
        else:
            return next(iter1, None)

    def next_e2():
        nonlocal leftover_e2
        if leftover_e2 is not None:
            next_val = leftover_e2
            leftover_e2 = None
            return next_val
        else:
            return next(iter2, None)

    while not ((current_e1 is None) and (current_e2 is None)):
        if current_e1 is None:
            append(result, current_e2)
            current_e2 = next_e2()
            continue
        if current_e2 is None:
            append(result, current_e1)
            current_e1 = next_e1()
            continue

        # Two spots
        if current_e1.is_spot and current_e2.is_spot:
            append(result, Spot(current_e1.x_start, current_e1.y - current_e2.y))
            current_e1 = next_e1()
            current_e2 = next_e2()
            continue

        # Two segments (Note: There cannot be one spot and one segment in the same iteration)
        # TODO PRove

        # Segments are guaranteed to start at the same time
        x_start = current_e1.x_start
        x_end = min(current_e1.x_end, current_e2.x_end)

        # If segments have equal length, compute subtraction
        if current_e1.x_end == current_e2.x_end:
            result_segment = Segment(x_start, current_e1.y_segment - current_e2.y_segment, x_end, current_e1.slope - current_e2.slope)
            append(result, result_segment)
            current_e1 = next_e1()
            current_e2 = next_e2()
            continue

        # Split longer segment, keep right part. Handle shorter segment
        if current_e1.x_end < current_e2.x_end:
            _, e2_right = current_e2.split_at(x_end)
            spot = Spot(x_end, current_e2.value_at(x_end))
            result_segment = Segment(x_start, current_e1.y_segment - current_e2.y_segment, x_end, current_e1.slope - current_e2.slope)
            append(result, result_segment)
            # We now need to consider the new spot in the next iteration,
            # and keep the right part of the longer segment for later
            current_e1 = next_e1()
            current_e2 = spot
            leftover_e2 = e2_right
            continue

        if current_e1.x_end > current_e2.x_end:
            _, e1_right = current_e1.split_at(x_end)
            spot = Spot(x_end, current_e1.value_at(x_end))
            result_segment = Segment(x_start, current_e1.y_segment - current_e2.y_segment, x_end, current_e1.slope - current_e2.slope)
            append(result, result_segment)
            # We now need to consider the new spot in the next iteration,
            # and keep the right part of the longer segment for later
            current_e1 = spot
            current_e2 = next_e2()
            leftover_e1 = e1_right
            continue

    return result