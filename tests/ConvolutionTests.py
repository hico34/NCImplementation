import unittest
from model.Piece import Piece
from model.PiecewiseLinearFunction import PiecewiseLinearFunction
from fractions import Fraction
from operations.Convolution import convolution, transient_periodic_convolution, periodic_convolution
from operations.Minimum import min_of_plfs
from helpers.util import lcm_fraction as lcm
import tests.testHelpers as testHelpers

class ConvolutionTests(unittest.TestCase):

    e1 = [
        Piece(Fraction(0), Fraction(0), Fraction(3), Fraction(2), Fraction(1)),
        Piece(Fraction(2), Fraction(5), Fraction(5), Fraction(4), Fraction(0)),
        Piece(Fraction(4), Fraction(5), Fraction(5), Fraction(6), Fraction(1))
    ]
    f1 = PiecewiseLinearFunction(e1, Fraction(2), Fraction(4), Fraction(2))
    e2 = [
        Piece(Fraction(0), Fraction(0), Fraction(0), Fraction(2), Fraction(2)),
        Piece(Fraction(2), Fraction(4), Fraction(4), Fraction(5), Fraction(0)),
        Piece(Fraction(5), Fraction(4), Fraction(4), Fraction(6), Fraction(3))
    ]
    f2 = PiecewiseLinearFunction(e2, Fraction(2), Fraction(4), Fraction(3))


    def test_convolution(self):
        f1 = testHelpers.uppFunction1
        f2 = testHelpers.uppFunction2
        g = convolution(f1, f2)
        print(f1.gg())
        print(f2.gg())
        print(g.gg())
    @unittest.skip
    def test_2(self):
        period = lcm(self.f1.period, self.f2.period)
        increment = period * min(self.f1.periodic_slope, self.f2.periodic_slope)
        g3 = transient_periodic_convolution(self.f2, self.f1)
        g4 = periodic_convolution(self.f1, self.f2, period, increment)
        g34 = min_of_plfs(g3, g4)

        x_values_f1, _ = testHelpers.relevant_x_values(g3)
        x_values_f2, _ = testHelpers.relevant_x_values(g4)
        x_values_g, periodic_part_x_values = testHelpers.relevant_x_values(g34)
        x_values = x_values_f1 + x_values_f2 + x_values_g
        x_values = list(dict.fromkeys(x_values))

        expected_values = []
        computed_values = []
        for i in range(len(x_values)):
            expected_values.append(min(g3.value_at(x_values[i]), g4.value_at(x_values[i])))
            computed_values.append(g34.value_at(x_values[i]))

        self.assertEqual(computed_values, expected_values)

        computed_periodic_values = []
        expected_periodic_values = []
        no_of_periods = 10

        periodic_x_values = []
        for i in range(no_of_periods):
            periodic_x_values = periodic_x_values + [x+g34.period * i for x in periodic_part_x_values]
        for x in periodic_x_values:
            expected_periodic_values.append(min(g3.value_at(x), g4.value_at(x)))
            computed_periodic_values.append(g34.value_at(x))

        self.assertEqual(computed_periodic_values, expected_periodic_values)

if __name__ == '__main__':
    unittest.main()