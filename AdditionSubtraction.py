from heapq import merge
from math import lcm
from collections import OrderedDict
from plfHelper import index_of_element_at
from Element import Element
from PiecewiseLinearFunction import PiecewiseLinearFunction

def add_plfs(f1, f2):
    if f1.rank > f2.rank:
        rank = f1.rank
    else:
        rank = f2.rank
    period = lcm(f1.period, f2.period)
    increment = (f1.increment / f1.period + f2.increment / f2.period) * period
    f1_extended_elements = f1.extend_and_get_all_elements(rank, period)
    f2_extended_elements = f2.extend_and_get_all_elements(rank, period)
    f1_extended_spots = list(map(lambda el: el.x_start, f1_extended_elements))
    f2_extended_spots = list(map(lambda el: el.x_start, f2_extended_elements))
    merged_spots = list(OrderedDict.fromkeys(merge(f1_extended_spots, f2_extended_spots)))
    result_elements = []
    for i in range(len(merged_spots)):
        x_start = merged_spots[i]
        y_spot = f1.value_at(x_start) + f2.value_at(x_start)
        f1_element = f1_extended_elements[index_of_element_at(f1_extended_elements, x_start)]
        f2_element = f2_extended_elements[index_of_element_at(f2_extended_elements, x_start)]
        y_segment = f1_element.y_segment + f2_element.y_segment
        slope = f1_element.slope + f2_element.slope
        if i == len(merged_spots) - 1:
            x_end = rank + period
        else:
            x_end = merged_spots[i+1]
        result_elements.append(Element(x_start, y_spot, y_segment, x_end, slope))
    return PiecewiseLinearFunction(result_elements, rank, period, increment)


