from Element import Element
from util import lcm_fraction as lcm
from PiecewiseLinearFunction import PiecewiseLinearFunction


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
    f1_elements = f1.extend_and_get_all_elements(rank, period)
    f2_elements = f2.extend_and_get_all_elements(rank, period)

    result_elements = []
    i = 0
    j = 0
    current_spot_x = 0
    while i < len(f1_elements) and j < len(f2_elements):
        f1_element = f1_elements[i]
        f2_element = f2_elements[j]
        print(i, j, current_spot_x, f1_element, f2_element)
        y_spot = min(f1_element.value_at(current_spot_x), f2_element.value_at(current_spot_x))
        next_spot_x = min(f1_element.x_end, f2_element.x_end)
        if f1_element.slope - f2_element.slope != 0:
            #TODO Prove Correctnes
            intersection_x = (f2_element.y_segment - f2_element.slope * f2_element.x_start - f1_element.y_segment + f1_element.slope*f1_element.x_start) / (f1_element.slope - f2_element.slope)
        else:
            intersection_x = -1
        if current_spot_x < intersection_x < next_spot_x:
            # Lower Element refers to the element with the lower limit at x_start.
            # Min(f1, f2) in the currently analysed interval will then be lower_element up to the intersection,
            # and upper_element after
            if f1_element.y_segment < f2_element.y_segment:
                lower_element = f1_element
                upper_element = f2_element
            else:
                lower_element = f2_element
                upper_element = f1_element
            result_elements.append(Element(current_spot_x, y_spot, lower_element.y_segment, intersection_x, lower_element.slope))
            intersection_y = f1_element.value_at(intersection_x)
            result_elements.append(
                Element(intersection_x, intersection_y, upper_element.y_segment, next_spot_x, upper_element.slope))
        elif f1_element.y_segment < f2_element.y_segment or (f1_element.y_segment == f2_element.y_segment and f1_element.slope < f2_element.slope):
            result_elements.append(
                Element(current_spot_x, y_spot, f1_element.y_segment, next_spot_x, f1_element.slope))
        else:
            result_elements.append(
                Element(current_spot_x, y_spot, f2_element.y_segment, next_spot_x, f2_element.slope))

        if f1_element.x_end < f2_element.x_end:
            i = i + 1
        elif f2_element.x_end < f1_element.x_end:
            j = j + 1
        else:
            i = i + 1
            j = j + 1
        current_spot_x = next_spot_x
        print(len(f1_elements), len(f2_elements), i, j, i < len(f1_elements) - 1 and i < len(f2_elements) - 1)
    return PiecewiseLinearFunction(result_elements, rank, period, increment)
