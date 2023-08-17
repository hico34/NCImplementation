from helpers.plfHelper import index_of_element_at
import math
from .Element import Element


class PiecewiseLinearFunction:
    def __init__(self, elements, rank, period, increment):
        if not (rank is None):
            self.transient_elements, self.periodic_elements = self.split_elements(elements, rank, period)
        else:
            self.transient_elements = elements
        self.all_elements = elements
        self.rank = rank
        self.period = period
        self.increment = increment
        self.periodic_slope = increment / period

    def value_at(self, x):
        if x < self.rank:
            i = index_of_element_at(self.transient_elements, x)
            if x == self.transient_elements[i].x_start:
                return self.transient_elements[i].y_spot
            else:
                return self.transient_elements[i].y_segment + (x - self.transient_elements[i].x_start) * \
                       self.transient_elements[i].slope
        else:
            if self.is_ultimately_affine():
                e = self.periodic_elements[0]
                return (x - e.x_start) * e.slope + e.y_segment
            no_of_periods = math.floor((x - (self.rank + self.period)) / self.period + 1)
            if no_of_periods < 0:
                no_of_periods = 0
            total_increment = no_of_periods * self.increment
            defined_value_at = x - no_of_periods * self.period

            i = index_of_element_at(self.periodic_elements, defined_value_at)
            if defined_value_at == self.periodic_elements[i].x_start:
                value = self.periodic_elements[i].y_spot
            else:
                value = self.periodic_elements[i].y_segment + (defined_value_at - self.periodic_elements[i].x_start) * \
                        self.periodic_elements[i].slope
            return value + total_increment

    def extend_and_get_all_elements(self, rank, period):
        if rank < self.rank or period % self.period != 0:
            print("Error at extend?")  # TODO
        if self.is_ultimately_affine():
            e = self.periodic_elements[0]
            extended_element = Element(e.x_start, e.y_spot, e.y_segment, rank + period, e.slope)
            return self.transient_elements + [extended_element]
        no_of_repeated_periods = math.ceil((rank + period - (self.rank + self.period)) / self.period)
        result_elements = self.transient_elements + self.periodic_elements
        for i in range(no_of_repeated_periods):
            for e in self.periodic_elements:
                result_elements.append(Element(e.x_start + self.period * (i + 1), e.y_spot + self.increment * (i + 1),
                                               e.y_segment + self.increment * (i + 1), e.x_end + self.period * (i + 1),
                                               e.slope))
        return self.cut_off(result_elements, rank + period)

    # Computes the supremum of deviations from the average slope of the periodic part (increment/period)
    def sup_deviation_from_periodic_slope(self):
        sup = 0
        for e in self.periodic_elements:
            sup = max(sup, e.y_spot - self.periodic_slope * e.x_start) #TODO Correct?
            sup = max(sup, e.y_segment - self.periodic_slope * e.x_start)
            sup = max(sup, (e.y_segment + e.slope * e.x_end) - self.periodic_slope * e.x_end)
        return sup

    # Computes the infimum of deviations from the average slope of the periodic part (increment/period)
    def inf_deviation_from_periodic_slope(self):
        inf = float("inf")
        for e in self.periodic_elements:
            inf = min(inf, e.y_spot - self.periodic_slope * e.x_start)
            inf = min(inf, e.y_segment - self.periodic_slope * e.x_start)
            inf = min(inf, (e.y_segment + e.slope * e.x_end) - self.periodic_slope * e.x_end)
        return inf

    def __str__(self):
        retStr = "{rank: " + str(self.rank) + ", period: " + str(self.period) + ", increment: " + str(
            self.increment) + "\n" + "TransEl:\n"
        for e in self.transient_elements:
            retStr = retStr + str(e) + "\n"
        retStr = retStr + "PerEl:\n"
        for e in self.periodic_elements:
            retStr = retStr + str(e) + "\n"
        return retStr

    # Splits the elements into transient and periodic parts at rank T,
    # and cuts off elements defined on x > T + d
    def split_elements(self, elements, rank, period):
        split_index = index_of_element_at(elements, rank)
        split_el = elements[split_index]
        if split_el.x_start == rank:
            transient_elements = elements[0:split_index]
            periodic_elements = self.cut_off(elements[split_index:], rank + period)
        else:
            left_element = Element(split_el.x_start, split_el.y_spot, split_el.y_segment, rank, split_el.slope)
            right_element = Element(rank, split_el.value_at(rank), split_el.value_at(rank), split_el.x_end,
                                    split_el.slope)
            transient_elements = elements[0:split_index] + [left_element]
            periodic_elements = self.cut_off([right_element] + elements[split_index + 1:], rank + period)
        return transient_elements, periodic_elements

    def cut_off(self, elements, end_x):
        last_index = index_of_element_at(elements, end_x)
        if last_index is None:
            last_index = len(elements) - 1
        last_element = elements[last_index]
        if last_element.x_start == end_x:
            return elements[0:last_index]
        else:
            last_element_cut = Element(last_element.x_start, last_element.y_spot, last_element.y_segment, end_x,
                                       last_element.slope)
            return elements[0:last_index] + [last_element_cut]

    def is_ultimately_affine(self):
        return len(self.periodic_elements) == 1

    def numpy_values_at(self, np_array):
        import numpy as np
        elements = self.extend_and_get_all_elements(np_array[np_array.size - 1] + self.period, 0)
        condlist = []
        funclist = []
        x = np_array
        for e in elements:
            condlist.append(x == e.x_start)
            funclist.append(e.y_spot)
            condlist.append(np.logical_and((e.x_start < x),(x < e.x_end)))
            funclist.append(lambda x, e=e: e.numpy_value_at(x))

        return np.piecewise(x, condlist, funclist)
