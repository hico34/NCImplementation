import unittest
from model.Piece import Piece
from model.PiecewiseLinearFunction import PiecewiseLinearFunction
from fractions import Fraction
from operations.Convolution import convolution
from operations.MaxPlusConvolution import maxplus_convolution
import tests.testHelpers as testHelpers
import itertools
from fractions import Fraction

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

    # This is an incredibly inefficient function to compute the value of the convolution at a specific time
    # It is slow but (barely) good enough for testing purposes
    def conv_value_at(self, f1: PiecewiseLinearFunction, f2: PiecewiseLinearFunction, x):
        x_values_f1 = []
        for e in f1.all_pieces:
            x_values_f1.append(x - e.x_start)
        x_values_f2 = []
        for e in f2.all_pieces:
            x_values_f2.append(e.x_start)
        x_values = [x] + x_values_f1 + x_values_f2
        x_values = list(dict.fromkeys(x_values))
        values = []
        for s in x_values:
            if 0 > s  or s > x:
                continue

            x1 = x-s
            i = Piece.index_of_piece_at(f1.all_pieces, x1)
            p = f1.all_pieces[i]
            if p.x_start < x1:
                left_limit_1 = p.value_at(x1)
                value_1 = p.value_at(x1)
                right_limit_1 = p.value_at(x1)
            elif x1 == 0:
                left_limit_1 = p.value_at(x1)
                value_1 = p.value_at(x1)
                right_limit_1 = p.lim_value_at(x1)
            else:
                left_limit_1 = f1.all_pieces[i-1].lim_value_at(x1)
                value_1 = p.value_at(x1)
                right_limit_1 = p.lim_value_at(x1)

            i = Piece.index_of_piece_at(f2.all_pieces, s)
            p = f2.all_pieces[i]
            if p.x_start < s:
                left_limit_2 = p.value_at(s)
                value_2 = p.value_at(s)
                right_limit_2 = p.value_at(s)
            elif s == 0:
                left_limit_2 = p.value_at(s)
                value_2 = p.value_at(s)
                right_limit_2 = p.lim_value_at(s)
            else:
                left_limit_2 = f2.all_pieces[i-1].lim_value_at(s)
                value_2 = p.value_at(s)
                right_limit_2 = p.lim_value_at(s)

            values.extend([left_limit_1+left_limit_2, value_1+value_2, right_limit_1+right_limit_2])
        return min(values)
    @unittest.skip
    def test_convolution(self):
        functions = testHelpers.test_functions
        function_tuples = itertools.permutations(functions, 2)
        i = 1
        for tuple in function_tuples:
            print(i)
            i += 1
            f1, f2 = tuple
            g = convolution(f1, f2)

            x_values_f1, _ = testHelpers.relevant_x_values(f1)
            x_values_f2, _ = testHelpers.relevant_x_values(f2)
            x_values_g, periodic_part_x_values = testHelpers.relevant_x_values(g)
            x_values = x_values_f1 + x_values_f2 + x_values_g
            x_values = list(dict.fromkeys(x_values))

            expected_values = []
            computed_values = []
            for i in range(len(x_values)):
                expected_values.append(self.conv_value_at(f1, f2, x_values[i]))
                computed_values.append(g.value_at(x_values[i]))

            self.assertEqual(computed_values, expected_values)

            computed_periodic_values = []
            expected_periodic_values = []
            no_of_periods = 2

            periodic_x_values = []
            for i in range(no_of_periods):
                periodic_x_values = periodic_x_values + [x+g.period * i for x in periodic_part_x_values]
            for x in periodic_x_values:
                expected_periodic_values.append(self.conv_value_at(f1, f2, x))
                computed_periodic_values.append(g.value_at(x))

            self.assertEqual(computed_periodic_values, expected_periodic_values)

    def test_2(self):
        functions = testHelpers.test_functions
        function_tuples = itertools.combinations(functions, 2)
        i = 1
        for tuple in function_tuples:
            print(i)
            i += 1
            if i <= 23:
                continue

            f1, f2 = tuple
            #gMin = convolution(f1, f2)
            gMax = maxplus_convolution(f1, f2)
            #print("var f1 = " + f1.gg())
            #print("var f2 = " + f2.gg())
            #print("var gMin = " + gMin.gg())
            #print("var gMax = " + gMax.gg())
            t =None

    def test_3(self):
        f1 = testHelpers.convexFunction2
        f2 = testHelpers.uppFunction1
        g = convolution(f1, f2)
        f1 = f1.extend(g.rank + g.period)
        f2 = f2.extend(g.rank + g.period)

        t, p = testHelpers.relevant_x_values(f1)
        x_values_f1 = t + p
        t, p = testHelpers.relevant_x_values(f2)
        x_values_f2 = t + p
        t, p = testHelpers.relevant_x_values(g)
        x_values_g = t + p
        x_values = x_values_f1 + x_values_f2 + x_values_g
        x_values = sorted(list(dict.fromkeys(x_values)))

        expected_values = []
        computed_values = []
        errors = []
        for i in range(len(x_values)):
            expected_value = self.conv_value_at(f1, f2, x_values[i])
            expected_values.append(expected_value)
            computed_value = g.value_at(x_values[i])
            computed_values.append(computed_value)
            if expected_value != computed_value:
                errors.append((x_values[i], expected_value, computed_value, expected_value - computed_value))
        self.assertEqual(computed_values, expected_values)



if __name__ == '__main__':
    unittest.main()