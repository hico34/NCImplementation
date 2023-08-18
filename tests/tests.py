import unittest
from operations.AdditionSubtraction import add_plfs
from operations.Minimum import min_of_plfs
import numpy as np
import tests.testHelpers as testHelpers
import itertools

class Test(unittest.TestCase):

    def test_value_at(self):
        functions = testHelpers.test_functions
        for f in functions:
            with self.subTest(f=f):
                x_values, periodic_part_x_values = testHelpers.relevant_x_values(f)

                computed_values = []
                for x in x_values:
                    computed_values.append(f.value_at(x))

                numpy_x_values = np.array(x_values)
                computed_values = np.array(computed_values)
                expected_values = f.numpy_values_at(numpy_x_values)
                self.assertTrue(np.array_equal(computed_values, expected_values))

                computed_periodic_values = []
                no_of_periods = 10
                periodic_x_values = []
                for i in range(no_of_periods):
                    l = [x+f.period * i for x in periodic_part_x_values]
                    periodic_x_values = periodic_x_values + l
                for x in periodic_x_values:
                    computed_periodic_values.append(f.value_at(x))

                computed_periodic_values = np.array(computed_periodic_values)
                numpy_periodic_x_values = np.array(periodic_x_values)
                expected_periodic_values = f.numpy_values_at(numpy_periodic_x_values)
                self.assertTrue(np.array_equal(computed_periodic_values, expected_periodic_values))

    def test_addition(self):
        functions = testHelpers.test_functions
        function_tuples = itertools.permutations(functions, 2)
        for tuple in function_tuples:
            f1, f2 = tuple
            g = add_plfs(f1, f2)

            x_values_f1, _ = testHelpers.relevant_x_values(f1)
            x_values_f2, _ = testHelpers.relevant_x_values(f2)
            x_values_g, periodic_x_values = testHelpers.relevant_x_values(g)
            x_values = x_values_f1 + x_values_f2 + x_values_g
            x_values = list(dict.fromkeys(x_values))

            expected_values = []
            computed_values = []
            # TODO Remove
            errors = []
            for i in range(len(x_values)):
                expected_values.append(f1.value_at(x_values[i]) + f2.value_at(x_values[i]))
                computed_values.append(g.value_at(x_values[i]))
                if(expected_values[i] != computed_values [i]):
                    errors.append((i, x_values[i], expected_values[i], computed_values[i]))
                    print(f1.value_at(x_values[i]), f2.value_at(x_values[i]), f1.value_at(x_values[i]) + f2.value_at(x_values[i]), g.value_at(x_values[i]))

            self.assertTrue(np.array_equal(computed_values, expected_values))

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

if __name__ == '__main__':
    unittest.main()