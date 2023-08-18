import unittest
from operations.MinimumMaximum import min_of_plfs
import numpy as np
import tests.testHelpers as testHelpers
import itertools

class MinMaxTests(unittest.TestCase):

    def test_minimum(self):
        functions = testHelpers.test_functions
        function_tuples = itertools.permutations(functions, 2)
        for tuple in function_tuples:
            f1, f2 = tuple
            g = min_of_plfs(f1, f2)

            x_values_f1, _ = testHelpers.relevant_x_values(f1)
            x_values_f2, _ = testHelpers.relevant_x_values(f2)
            x_values_g, periodic_x_values = testHelpers.relevant_x_values(g)
            x_values = x_values_f1 + x_values_f2 + x_values_g
            x_values = list(dict.fromkeys(x_values))

            expected_values = []
            computed_values = []
            for i in range(len(x_values)):
                expected_values.append(min(f1.value_at(x_values[i]), f2.value_at(x_values[i])))
                computed_values.append(g.value_at(x_values[i]))

            self.assertTrue(np.array_equal(computed_values, expected_values))