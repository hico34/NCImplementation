from math import lcm, gcd
from fractions import Fraction
from model.Piece import Piece
from model.Element import Element
from model.Segment import Segment
from .plfHelper import index_of_piece_at
from fractions import Fraction


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
def append(list: [Element], e: Element):
    if e.x_start == Fraction(13, 2):
        t = None
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

def cut_off(elements, end_x):
    # TODO Auslagern, Binary Search
    last_index = None
    for i in range(len(elements)):
        if elements[i].is_segment and elements[i].x_start <= end_x < elements[i].x_end:
            last_index = i
            break
        elif elements[i].is_spot and elements[i].x_start == end_x:
            last_index = i
            break


    if last_index is None:
        last_index = len(elements) - 1
    last_piece = elements[last_index]
    if last_piece.x_start == end_x:
        return elements[0:last_index]
    else:
        last_piece_cut = Segment(last_piece.x_start, last_piece.y_segment, end_x, last_piece.slope)
        return elements[0:last_index] + [last_piece_cut]

