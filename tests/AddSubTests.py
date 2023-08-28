import unittest
from operations.Addition import add_functions
from operations.Subtraction import subtract_functions
import tests.testHelpers as testHelpers
import itertools


class Test(unittest.TestCase):

    def test_addition(self):
        functions = testHelpers.test_functions
        function_tuples = itertools.combinations(functions, 2)
        for tuple in function_tuples:
            f1, f2 = tuple
            g = add_functions(f1, f2)

            x_values_f1, _ = testHelpers.relevant_x_values(f1)
            x_values_f2, _ = testHelpers.relevant_x_values(f2)
            x_values_g, periodic_part_x_values = testHelpers.relevant_x_values(g)
            x_values = x_values_f1 + x_values_f2 + x_values_g
            x_values = list(dict.fromkeys(x_values))

            expected_values = []
            computed_values = []
            for i in range(len(x_values)):
                expected_values.append(f1.value_at(x_values[i]) + f2.value_at(x_values[i]))
                computed_values.append(g.value_at(x_values[i]))

            self.assertEqual(computed_values, expected_values)

            computed_periodic_values = []
            expected_periodic_values = []
            no_of_periods = 10

            periodic_x_values = []
            for i in range(no_of_periods):
                periodic_x_values = periodic_x_values + [x+g.period * i for x in periodic_part_x_values]
            for x in periodic_x_values:
                expected_periodic_values.append(f1.value_at(x) + f2.value_at(x))
                computed_periodic_values.append(g.value_at(x))

            self.assertEqual(computed_periodic_values, expected_periodic_values)

    def test_subtraction(self):
        functions = testHelpers.test_functions
        function_tuples = itertools.combinations(functions, 2)
        for tuple in function_tuples:
            f1, f2 = tuple
            g = subtract_functions(f1, f2)

            x_values_f1, _ = testHelpers.relevant_x_values(f1)
            x_values_f2, _ = testHelpers.relevant_x_values(f2)
            x_values_g, periodic_part_x_values = testHelpers.relevant_x_values(g)
            x_values = x_values_f1 + x_values_f2 + x_values_g
            x_values = list(dict.fromkeys(x_values))

            expected_values = []
            computed_values = []
            for i in range(len(x_values)):
                expected_values.append(f1.value_at(x_values[i]) - f2.value_at(x_values[i]))
                computed_values.append(g.value_at(x_values[i]))

            self.assertEqual(computed_values, expected_values)

            computed_periodic_values = []
            expected_periodic_values = []
            no_of_periods = 10

            periodic_x_values = []
            for i in range(no_of_periods):
                periodic_x_values = periodic_x_values + [x+g.period * i for x in periodic_part_x_values]
            for x in periodic_x_values:
                expected_periodic_values.append(f1.value_at(x) - f2.value_at(x))
                computed_periodic_values.append(g.value_at(x))

            self.assertEqual(computed_periodic_values, expected_periodic_values)


if __name__ == '__main__':
    unittest.main()
