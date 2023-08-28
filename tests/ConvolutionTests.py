import unittest
from model.PiecewiseLinearFunction import PiecewiseLinearFunction
from operations.Convolution import convolution
from operations.MaxPlusConvolution import maxplus_convolution
import tests.testHelpers as testHelpers
import itertools
from operations.Minimum import minimum
from operations.Maximum import maximum

class ConvolutionTests(unittest.TestCase):

    # Checks if two given functions are equal, even if they are not represented equally
    def function_equality(self, f: PiecewiseLinearFunction, g: PiecewiseLinearFunction):
        x_f_transient, x_f_periodic = testHelpers.relevant_x_values(f)
        x_g_transient, x_g_periodic = testHelpers.relevant_x_values(g)
        x_values = x_f_transient + x_g_transient
        periodic_part_x_values = x_g_periodic + x_f_periodic
        x_values = list(dict.fromkeys(x_values))

        for i in range(len(x_values)):
            if f.value_at(x_values[i]) != g.value_at(x_values[i]):
                print("Inequality at ({}, {} != {})".format(x_values[i], f.value_at(x_values[i]), g.value_at(x_values[i])))
                return False

        no_of_periods = 10

        periodic_x_values = []
        for i in range(no_of_periods):
            periodic_x_values = periodic_x_values + [x+g.period * i for x in periodic_part_x_values]
        for x in periodic_x_values:
            if f.value_at(x) != g.value_at(x):
                print("Inequality at ({}, {} != {}".format(x, f.value_at(x), g.value_at(x)))
                return False

        return True

    def test_convolution_commutativity(self):
        functions = testHelpers.test_functions
        function_tuples = itertools.combinations(functions, 2)
        for tuple in function_tuples:
            f1, f2 = tuple

            g1 = convolution(f1, f2)
            g2 = convolution(f2, f1)
            self.assertTrue(self.function_equality(g1, g2))

    def test_convolution_associativity(self):
        functions = testHelpers.test_functions
        function_tuples = itertools.combinations(functions, 3)
        for tuple in function_tuples:
            f1, f2, f3 = tuple

            g1 = convolution(convolution(f1, f2), f3)
            g2 = convolution(f1, convolution(f2, f3))
            self.assertTrue(self.function_equality(g1, g2))

    def test_convolution_distributivity(self):
        functions = testHelpers.test_functions
        function_tuples = itertools.combinations(functions, 3)
        for tuple in function_tuples:
            f1, f2, f3 = tuple

            g1 = convolution(f1, minimum(f2, f3))
            g2 = minimum(convolution(f1, f2), convolution(f1, f3))
            self.assertTrue(self.function_equality(g1, g2))

    def test_maxplus_convolution_commutativity(self):
        functions = testHelpers.test_functions
        function_tuples = itertools.combinations(functions, 2)
        for tuple in function_tuples:
            f1, f2 = tuple
            print(f1.rank, f1.period, f1.increment)
            print(f2.rank, f2.period, f2.increment)
            g1 = maxplus_convolution(f1, f2)
            g2 = maxplus_convolution(f2, f1)
            self.assertTrue(self.function_equality(g1, g2))

    def test_maxplus_convolution_associativity(self):
        functions = testHelpers.test_functions
        function_tuples = itertools.combinations(functions, 3)
        for tuple in function_tuples:
            f1, f2, f3 = tuple

            g1 = maxplus_convolution(maxplus_convolution(f1, f2), f3)
            g2 = maxplus_convolution(f1, maxplus_convolution(f2, f3))
            self.assertTrue(self.function_equality(g1, g2))

    def test_maxplus_convolution_distributivity(self):
        functions = testHelpers.test_functions
        function_tuples = itertools.combinations(functions, 3)
        for tuple in function_tuples:
            f1, f2, f3 = tuple

            g1 = maxplus_convolution(f1, maximum(f2, f3))
            g2 = maximum(maxplus_convolution(f1, f2), maxplus_convolution(f1, f3))
            self.assertTrue(self.function_equality(g1, g2))

if __name__ == '__main__':
    unittest.main()