from plfHelper import index_of_element_at
import math


class PiecewiseLinearFunction:
    def __init__(self, elements, rank, period, increment):
        i = index_of_element_at(elements, rank)
        self.transient_elements = elements[0:i]
        self.periodic_elements = elements[i:]
        self.rank = rank
        self.period = period
        self.increment = increment

    def value_at(self, x):
        if x < self.rank:
            i = index_of_element_at(self.transient_elements, x)
            if x == self.transient_elements[i].x_start:
                return self.transient_elements[i].y_spot
            else:
                return self.transient_elements[i].y_segment + (x - self.transient_elements[i].x_start) * \
                       self.transient_elements[i].slope
        else:
            no_of_periods = math.floor((x - (self.rank + self.period)) / self.period + 1)
            if no_of_periods < 0:
                no_of_periods = 0
            total_increment = no_of_periods * self.increment
            defined_value_at = x - no_of_periods * self.period

            print("periods: " + str(no_of_periods))
            print("increment: " + str(total_increment))
            print("valueAt: " + str(defined_value_at))

            i = index_of_element_at(self.periodic_elements, defined_value_at)
            if defined_value_at == self.periodic_elements[i].x_start:
                value = self.periodic_elements[i].y_spot
            else:
                value = self.periodic_elements[i].y_segment + (defined_value_at - self.periodic_elements[i].x_start) * \
                        self.periodic_elements[i].slope
            print("return: " + str(value + total_increment))
            return value + total_increment

    def extend_and_get_all_elements(self, rank, period):
        if self.rank < rank | period % self.period != 0:
            return None
        no_of_repeated_periods = round((rank + period - (self.rank + self.period))/period)
        return self.transient_elements + self.periodic_elements + (self.periodic_elements * no_of_repeated_periods)


    def __str__(self):
        retStr = "{rank: " + str(self.rank) + ", period: " + str(self.period) + ", increment: " + str(self.increment) + "\n" + "TransEl:\n"
        for e in self.transient_elements:
            retStr = retStr + str(e) + "\n"
        retStr = retStr + "PerEl:\n"
        for e in self.periodic_elements:
            retStr = retStr + str(e) + "\n"
        return retStr
