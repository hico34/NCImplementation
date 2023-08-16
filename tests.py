import unittest
from PiecewiseLinearFunction import PiecewiseLinearFunction
from AdditionSubtraction import add_plfs
from MinimumMaximum import min_of_plfs
from Element import Element
from fractions import Fraction
import numpy as np

class Test(unittest.TestCase):

    def test_value_at(self):
        f1 = PiecewiseLinearFunction()
        x_values = []
        periodic_x_values = []
        computed_values = []
        for e in f1.all_elements:
            x_values.append(e.x_start)
            x_within_segment = (e.x_end - e.x_start) / 2
            x_values.append(x_within_segment)
            if e.x_start >= f1.rank:
                periodic_x_values.append(e.x_start)
                periodic_x_values.append(x_within_segment)
            computed_values.append(e.value_at(e.x_start))
            computed_values.append(e.value_at(x_within_segment))

        numpy_x_values = np.array(x_values)
        numpy_periodic_x_values = np.array(periodic_x_values)
        self.assertEqual(computed_values, f1.numpy_values_at(numpy_x_values))


        computed_periodic_values = []
        no_of_periods = 10
        for i in range(1, no_of_periods):
            periodic_x_values = periodic_x_values + (periodic_x_values + f1.period)
        for x in periodic_x_values:
            computed_periodic_values.append(f1.value_at(x))
        self.assertEqual(computed_periodic_values, f1.numpy_values_at(numpy_periodic_x_values))

    def test_addition(self):
        f1 = PiecewiseLinearFunction()
        f2 = PiecewiseLinearFunction()
        g = add_plfs(f1, f2)

        x_values = []
        periodic_x_values = []
        for e in f1.all_elements:
            x_values.append(e.x_start)
            x_within_segment = (e.x_end - e.x_start) / 2
            x_values.append(x_within_segment)
            if e.x_start >= f1.rank:
                periodic_x_values.append(e.x_start)
                periodic_x_values.append(x_within_segment)
        for e in f2.all_elements:
            x_values.append(e.x_start)
            x_within_segment = (e.x_end - e.x_start) / 2
            x_values.append(x_within_segment)
            if e.x_start >= f2.rank:
                periodic_x_values.append(e.x_start)
                periodic_x_values.append(x_within_segment)

        computed_values = []
        numpy_x_values = np.array(x_values)
        numpy_values_f1 = f1.numpy_values_at(numpy_x_values)
        numpy_values_f2 = f2.numpy_values_at(numpy_x_values)
        expected_values = []
        for x in x_values:
            computed_values.append(g.value_at(x))
        for i in range(len(x_values) - 1):
            expected_values.append(numpy_values_f1[i] + numpy_values_f2[i])
        self.assertEqual(expected_values, computed_values)

    def test_minimum(self):
        elementList = [
            Element(Fraction(0), Fraction(0), Fraction(0), Fraction(3), Fraction(.5)),
            Element(Fraction(3), Fraction(1.5), Fraction(1.5), Fraction(5), Fraction(1)),
            Element(Fraction(5), Fraction(7), Fraction(3.5), Fraction(8), Fraction(1.5)),
            Element(Fraction(8), Fraction(10.5), Fraction(10.5), Fraction(9), Fraction(1)),
            Element(Fraction(9), Fraction(11.5), Fraction(11.5), Fraction(11), Fraction(2))
        ]


        elementList2 = [
            Element(Fraction(0), Fraction(0), Fraction(0), Fraction(3), Fraction(.5)),
            Element(Fraction(3), Fraction(1.5), Fraction(1.5), Fraction(5), Fraction(1)),
            Element(Fraction(5), Fraction(7), Fraction(3.5), Fraction(8), Fraction(1.5)),
            Element(Fraction(8), Fraction(10.5), Fraction(10.5), Fraction(10), Fraction(2)),
            Element(Fraction(10), Fraction(12.5), Fraction(11.5), Fraction(14), Fraction(4))
        ]

        f1 = PiecewiseLinearFunction(elementList, Fraction(8), Fraction(3), Fraction(5))
        f2 = PiecewiseLinearFunction(elementList2, Fraction(8), Fraction(6), Fraction(20))
        g = min_of_plfs(f1, f2)

        x_values = []
        periodic_x_values = []
        for e in f1.all_elements:
            x_values.append(e.x_start)
            x_within_segment = (e.x_end - e.x_start) / 2
            x_values.append(x_within_segment)
            if e.x_start >= f1.rank:
                periodic_x_values.append(e.x_start)
                periodic_x_values.append(x_within_segment)
        for e in f2.all_elements:
            x_values.append(e.x_start)
            x_within_segment = (e.x_end - e.x_start) / 2
            x_values.append(x_within_segment)
            if e.x_start >= f2.rank:
                periodic_x_values.append(e.x_start)
                periodic_x_values.append(x_within_segment)
        for e in g.all_elements:
            x_values.append(e.x_start)
            x_within_segment = (e.x_end - e.x_start) / 2
            x_values.append(x_within_segment)
            if e.x_start >= g.rank:
                periodic_x_values.append(e.x_start)
                periodic_x_values.append(x_within_segment)

        computed_values = []
        numpy_x_values = np.array(x_values)
        numpy_periodic_x_values = np.array(periodic_x_values)
        numpy_values_f1 = f1.numpy_values_at(numpy_x_values)
        numpy_values_f2 = f2.numpy_values_at(numpy_x_values)
        expected_values = []
        for x in x_values:
            computed_values.append(g.value_at(x))
        for i in range(len(x_values) - 1):
            expected_values.append(min(numpy_values_f1[i], numpy_values_f2[i]))
        self.assertEqual(expected_values, computed_values)