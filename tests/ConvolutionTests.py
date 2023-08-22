import unittest
from model.Piece import Piece
from model.PiecewiseLinearFunction import PiecewiseLinearFunction
from model.Spot import Spot
from fractions import Fraction
from operations.Convolution import convolution
import tests.testHelpers as testHelpers
import itertools

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
    # It is slow but good enough for testing purposes
    def conv_value_at(self, f1: PiecewiseLinearFunction, f2: PiecewiseLinearFunction, x):
        if x > f1.rank + f1.period:
            f1 = f1.extend(x)
        if x > f2.rank + f2.period:
            f2 = f2.extend(x)

        f1_value_at_x = f1.value_at(x)

        t, p = f1.decompose()
        e1 = t + p
        t, p = f2.decompose()
        e2 = t + p

        result = []
        iter1 = iter(e1)
        iter2 = iter(e2)

        current_e1 = next(iter1, None)
        current_e2 = next(iter2, None)

        leftover_e1 = None
        leftover_e2 = None

        # Cheats leftover values into the iterator
        def next_e1():
            nonlocal leftover_e1
            if leftover_e1 is not None:
                next_val = leftover_e1
                leftover_e1 = None
                return next_val
            else:
                return next(iter1, None)

        def next_e2():
            nonlocal leftover_e2
            if leftover_e2 is not None:
                next_val = leftover_e2
                leftover_e2 = None
                return next_val
            else:
                return next(iter2, None)

        while current_e1.x_start <= x and (current_e1 is not None) and (current_e2 is not None):

            if current_e1.x_end > x and current_e2.x_end > x:
                result.append(current_e2.lim_value_at(current_e1.x_start) - current_e1.lim_value_at(current_e1.x_start) + f1_value_at_x)
                result.append(current_e2.lim_value_at(x) - current_e1.lim_value_at(x) + f1_value_at_x)
                break

            if current_e1 is None or current_e2 is None:
                t = None
            # Two spots
            if current_e1.is_spot and current_e2.is_spot:
                result.append(current_e2.y - current_e1.y + f1_value_at_x)
                current_e1 = next_e1()
                current_e2 = next_e2()
                continue

            # Two segments (Note: There cannot be one spot and one segment in the same iteration)
            # TODO PRove

            # Segments are guaranteed to start at the same time
            x_start = current_e1.x_start
            x_end = min(current_e1.x_end, current_e2.x_end)

            # If segments have equal length, compute potential infimums
            if current_e1.x_end == current_e2.x_end:
                result.append(current_e2.lim_value_at(x_start) - current_e1.lim_value_at(x_start) + f1_value_at_x)
                result.append(current_e2.lim_value_at(x_end) - current_e1.lim_value_at(x_end) + f1_value_at_x)
                current_e1 = next_e1()
                current_e2 = next_e2()
                continue

            # Split longer segment, keep right part. Handle shorter segment
            if current_e1.x_end < current_e2.x_end:
                _, e2_right = current_e2.split_at(x_end)
                spot = Spot(x_end, current_e2.value_at(x_end))
                result.append(current_e2.lim_value_at(x_start) - current_e1.lim_value_at(x_start) + f1_value_at_x)
                result.append(current_e2.lim_value_at(x_end) - current_e1.lim_value_at(x_end) + f1_value_at_x)
                # We now need to consider the new spot in the next iteration,
                # and keep the right part of the longer segment for later
                current_e1 = next_e1()
                current_e2 = spot
                leftover_e2 = e2_right
                continue

            if current_e1.x_end > current_e2.x_end:
                _, e1_right = current_e1.split_at(x_end)
                spot = Spot(x_end, current_e1.value_at(x_end))
                result.append(current_e2.lim_value_at(x_start) - current_e1.lim_value_at(x_start) + f1_value_at_x)
                result.append(current_e2.lim_value_at(x_end) - current_e1.lim_value_at(x_end) + f1_value_at_x)
                # We now need to consider the new spot in the next iteration,
                # and keep the right part of the longer segment for later
                current_e1 = spot
                current_e2 = next_e2()
                leftover_e1 = e1_right
                continue

        result = min(result)
        return result

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
        f1 = testHelpers.uppFunction2
        f2 = testHelpers.uppFunction1
        g = convolution(f1, f2)
        print("var f1 = " + f1.gg())
        print("var f2 = " + f2.gg())
        print("var g = " + g.gg())


if __name__ == '__main__':
    unittest.main()