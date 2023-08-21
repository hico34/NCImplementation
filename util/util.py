from math import lcm, gcd
from model.Element import Element
from model.Segment import Segment
from fractions import Fraction


# Find the least common multiple of 2 fractions
def lcm_fraction(fr1, fr2):
    num = lcm(fr1.numerator, fr2.numerator)
    den = gcd(fr1.denominator, fr2.denominator)
    return Fraction(num, den)

# TODO mention
# If possible, merge segments to avoid unnecessary elements
def append(list: [Element], e: Element):
    if len(list) >= 2 and e.is_segment:
        last_el = list[-1]
        second_to_last_el = list[-2]
    else:
        list.append(e)
        return

    if not (last_el.is_spot and second_to_last_el.is_segment):
        list.append(e)
        return

    is_continuous = second_to_last_el.lim_value_at(last_el.x_start) == last_el.y
    is_continuous = is_continuous and second_to_last_el.x_end == last_el.x_start
    is_continuous = is_continuous and last_el.y == e.lim_value_at(last_el.x_start)
    is_continuous = is_continuous and last_el.x_end == e.x_start
    if is_continuous and second_to_last_el.slope == e.slope:
        merged_segment = Segment(second_to_last_el.x_start, second_to_last_el.y_segment, e.x_end, e.slope)
        list.pop()
        list[-1] = merged_segment
    else:
        list.append(e)

