from util.util import lcm_fraction as lcm
from util.util import append
from model.PiecewiseLinearFunction import PiecewiseLinearFunction
from model.Element import Element
from model.Spot import Spot
import math
from typing import List


def maximum(f1: PiecewiseLinearFunction, f2: PiecewiseLinearFunction):
    # Precompute rank
    if f1.increment == -math.inf:
        period = f2.period
        increment = f2.increment
        rank = max(f1.rank, f2.rank)
    elif f2.increment == -math.inf:
        period = f1.period
        increment = f1.increment
        rank = max(f1.rank, f2.rank)
    elif f1.periodic_slope > f2.periodic_slope:
        period = f1.period
        increment = f1.increment
        M1 = f2.sup_deviation_from_periodic_slope()
        m2 = f1.inf_deviation_from_periodic_slope()
        rank = max((M1-m2)/(f1.periodic_slope - f2.periodic_slope), f1.rank, f2.rank)
    elif f2.periodic_slope > f1.periodic_slope:
        period = f2.period
        increment = f2.increment
        M1 = f1.sup_deviation_from_periodic_slope()
        m2 = f2.inf_deviation_from_periodic_slope()
        rank = max((M1-m2)/(f2.periodic_slope - f1.periodic_slope), f1.rank, f2.rank)
    else:
        period = lcm(f1.period, f2.period)
        increment = lcm(f1.period, f2.period) * f1.periodic_slope
        rank = max(f1.rank, f2.rank)

    t, p = f1.extend(rank + period).decompose()
    f1_elements = t + p
    t, p = f2.extend(rank + period).decompose()
    f2_elements = t + p
    result_elements = max_of_elements(f1_elements, f2_elements)

    return PiecewiseLinearFunction.from_elements(result_elements, rank, period, increment)


# Requires lists sorted by x_start, and spots < segments if both start at the same value
# Elements in the same list may not overlap
def max_of_elements(e1: [Element], e2: [Element]):
    result = []
    iter1 = iter(e1)
    iter2 = iter(e2)

    current_e1 = next(iter1, None)
    current_e2 = next(iter2, None)

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

        # No overlap
        if current_e1.x_end < current_e2.x_start:
            append(result, current_e1)
            current_e1 = next_e1()
            continue
        elif current_e2.x_end < current_e1.x_start:
            append(result, current_e2)
            current_e2 = next_e2()
            continue
        elif current_e1.is_segment:
            if current_e1.x_end == current_e2.x_start:
                append(result, current_e1)
                current_e1 = next_e1()
                continue
            elif current_e1.x_start == current_e2.x_end:
                append(result, current_e2)
                current_e2 = next_e2()
                continue
        elif current_e2.is_segment:
            if current_e2.x_end == current_e1.x_start:
                append(result, current_e2)
                current_e2 = next_e2()
                continue
            elif current_e2.x_start == current_e1.x_end:
                append(result, current_e1)
                current_e1 = next_e1()
                continue

        # Two spots
        if current_e1.is_spot and current_e2.is_spot:
            append(result, Spot(current_e1.x_start, max(current_e1.y, current_e2.y)))
            current_e1 = next_e1()
            current_e2 = next_e2()
            continue

        # One segment, one spot
        if current_e1.is_spot and current_e2.is_segment:
            # If the spot is not part of the upper envelope, we can disregard it and continue with next iteration
            if current_e2.value_at(current_e1.x_start) >= current_e1.y:
                current_e1 = next_e1()
                continue

            # Split segment at spot, keep the right part for the next iteration
            left_segment, right_segment = current_e2.split_at(current_e1.x_start)
            spot = Spot(current_e1.x_start, max(current_e1.y, current_e2.value_at(current_e1.x_start)))
            append(result, left_segment)
            append(result, spot)
            current_e1 = next_e1()
            current_e2 = right_segment
            continue

        elif current_e2.is_spot and current_e1.is_segment:
            # If the spot is not part of the upper envelope, we can disregard it and continue with next iteration
            if current_e1.value_at(current_e2.x_start) >= current_e2.y:
                current_e2 = next_e2()
                continue

            # Split segment at spot, keep the right part for the next iteration
            left_segment, right_segment = current_e1.split_at(current_e2.x_start)
            spot = Spot(current_e2.x_start, max(current_e2.y, current_e1.value_at(current_e2.x_start)))
            append(result, left_segment)
            append(result, spot)
            current_e1 = right_segment
            current_e2 = next_e2()
            continue

        # Two segments

        # If one segment starts earlier, split the earlier segment and keep its right part for the next iteration
        if current_e1.x_start < current_e2.x_start:
            left_segment, right_segment = current_e1.split_at(current_e2.x_start)
            spot = Spot(current_e2.x_start, current_e1.value_at(current_e2.x_start))
            append(result, left_segment)
            append(result, spot)
            current_e1 = right_segment
            continue
        elif current_e2.x_start < current_e1.x_start:
            left_segment, right_segment = current_e2.split_at(current_e1.x_start)
            spot = Spot(current_e1.x_start, current_e2.value_at(current_e1.x_start))
            append(result, left_segment)
            append(result, spot)
            current_e2 = right_segment
            continue

        # Segments are now guaranteed to start at the same time
        overlap_start = current_e1.x_start
        overlap_end = min(current_e1.x_end, current_e2.x_end)
        # Compute intersection within overlap
        if current_e1.slope != current_e2.slope:
            intersection_x = (current_e2.y_segment - current_e2.slope * current_e2.x_start - current_e1.y_segment + current_e1.slope*current_e1.x_start) / (current_e1.slope - current_e2.slope)
            if overlap_start < intersection_x < overlap_end:
                intersection_y = current_e1.value_at(intersection_x)
            else:
                intersection_x = None
        else:
            intersection_x = None

        # Determine upper segment at time of overlap_start
        if current_e1.lim_value_at(overlap_start) < current_e2.lim_value_at(overlap_start) or (current_e1.lim_value_at(overlap_start) == current_e2.lim_value_at(overlap_start) and current_e1.slope < current_e2.slope):
            lower = 1
            lower_e = current_e1
            upper = 2
            upper_e = current_e2
        else:
            lower = 2
            lower_e = current_e2
            upper = 1
            upper_e = current_e1

        # Split segments at intersection, keep right parts for next iteration
        if intersection_x is not None:
            left_lower, right_lower = lower_e.split_at(intersection_x)
            spot = Spot(intersection_x, intersection_y)
            left_upper, right_upper = upper_e.split_at(intersection_x)
            append(result, left_upper)
            append(result, spot)
            if lower == 1:
                current_e1 = right_lower
                current_e2 = right_upper
            elif lower == 2:
                current_e1 = right_upper
                current_e2 = right_lower
            continue

        if lower_e.x_end == upper_e.x_end:
            append(result, upper_e)
            current_e1 = next_e1()
            current_e2 = next_e2()
            continue

        # Split longer segment, keep right part. Handle shorter segment
        if lower_e.x_end < upper_e.x_end:
            upper_left, upper_right = upper_e.split_at(lower_e.x_end)
            spot = Spot(lower_e.x_end, upper_e.value_at(lower_e.x_end))
            append(result, upper_left)
            # Since the next element might be defined on the support of the spot,
            # we need to consider the spot in the next iteration and keep upper_right for later
            if lower == 1:
                current_e1 = next_e1()
                current_e2 = spot
                leftover_e2 = upper_right
            if lower == 2:
                current_e1 = spot
                current_e2 = next_e2()
                leftover_e1 = upper_right
            continue

        if upper_e.x_end < lower_e.x_end:
            _, lower_right = lower_e.split_at(upper_e.x_end)
            spot = Spot(upper_e.x_end, lower_e.value_at(upper_e.x_end))
            append(result, upper_e)
            # Since the next element might be defined on the support of the spot,
            # we need to consider the spot in the next iteration and keep lower_right for later
            if upper == 1:
                current_e1 = next_e1()
                current_e2 = spot
                leftover_e2 = lower_right
            if upper == 2:
                current_e1 = spot
                current_e2 = next_e2()
                leftover_e1 = lower_right
            continue

    return result


# Divide and conquer approach to computing the minimum of a set of unsorted elements
# Expects a list of lists of elements (containing a single Element when not calling recursively)
def max_of_unsorted_elements(elements: List[List[Element]]):
    if len(elements) == 1:
        return elements[0]
    elif len(elements) == 2:
        return max_of_elements(elements[0], elements[1])
    else:
        split_i = len(elements) // 2
        left = max_of_unsorted_elements(elements[:split_i])
        right = max_of_unsorted_elements(elements[split_i:])
        return max_of_elements(left, right)
