from math import lcm, gcd
from fractions import Fraction
from model.Piece import Piece
from model.Element import Element
from model.Segment import Segment


# Find the least common multiple of 2 fractions
def lcm_fraction(fr1, fr2):
    num = lcm(fr1.numerator, fr2.numerator)
    den = gcd(fr1.denominator, fr2.denominator)
    return Fraction(num, den)


def gcd_fraction(fr1, fr2):
    num = gcd(fr1.numerator, fr2.numerator)
    den = lcm(fr1.denominator, fr2.denominator)
    return Fraction(num, den)

def decompose(pieces: [Piece]):
    decomposed_list = []
    for e in pieces:
        spot, segment = e.decompose()
        decomposed_list.append(spot)
        decomposed_list.append(segment)
    return decomposed_list

def compose(elements):
    result_pieces = []
    spot = None
    segment = None
    for e in elements:
        if e.is_spot:
            spot = e
        if e.is_segment:
            segment = e
        if (spot is not None) and (segment is not None):
            piece = Piece(spot.x_start, spot.y, segment.y_segment, segment.x_end, segment.slope)
            result_pieces.append(piece)
            spot = None
            segment = None
    return result_pieces

# TODO mention
# If possible, merge segments to avoid unnecessary elements
def append_segment(list: [Element], segment: Segment):
    if len(list) >= 2:
        last_el = list[-1]
        second_to_last_el = list[-2]
    else:
        list.append(segment)
        return

    if not (last_el.is_spot and second_to_last_el.is_segment):
        list.append(segment)
        return

    is_continuous = second_to_last_el.lim_value_at(last_el.x_start) == last_el.y
    is_continuous = is_continuous and second_to_last_el.x_end == last_el.x_start
    is_continuous = is_continuous and last_el.y == segment.lim_value_at(last_el.x_start)
    is_continuous = is_continuous and last_el.x_end == segment.x_start
    if is_continuous and second_to_last_el.slope == segment.slope:
        merged_segment = Segment(second_to_last_el.x_start, second_to_last_el.y_segment, segment.x_end, segment.slope)
        list.pop()
        list[-1] = merged_segment
    else:
        list.append(segment)

