import unittest
import numpy as np
import tests.testHelpers as testHelpers

class Test(unittest.TestCase):

    def numpy_piece_value_at(self, p, list):
        values = np.array([])
        for x in list:
            values = np.append(values, [p.value_at(x)])
        return values

    def numpy_values_at(self, f, np_array):
        pieces = f.extend(np_array[np_array.size - 1] + f.period).all_pieces
        condlist = []
        funclist = []
        x = np_array
        for e in pieces:
            condlist.append(x == e.x_start)
            funclist.append(e.y_spot)
            condlist.append(np.logical_and((e.x_start < x), (x < e.x_end)))
            funclist.append(lambda x, e=e: self.numpy_piece_value_at(e, x))

        return np.piecewise(x, condlist, funclist)

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
                expected_values = self.numpy_values_at(f, numpy_x_values)
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
                expected_periodic_values = self.numpy_values_at(f, numpy_periodic_x_values)
                self.assertTrue(np.array_equal(computed_periodic_values, expected_periodic_values))

    def test_is_concave(self):
        self.assertTrue(testHelpers.concaveFunction1.is_concave())
        self.assertTrue(testHelpers.concaveFunction2.is_concave())
        self.assertFalse(testHelpers.convexFunction1.is_concave())
        self.assertFalse(testHelpers.convexFunction2.is_concave())
        self.assertFalse(testHelpers.continuousFunction1.is_concave())
        self.assertFalse(testHelpers.continuousFunction2.is_concave())
        self.assertFalse(testHelpers.uppFunction1.is_concave())
        self.assertFalse(testHelpers.uppFunction2.is_concave())
        self.assertFalse(testHelpers.ultimatelyAffineFunction1.is_concave())
        self.assertFalse(testHelpers.ultimatelyAffineFunction1.is_concave())
        
    def test_is_convex(self):
        self.assertTrue(testHelpers.convexFunction1.is_convex())
        self.assertTrue(testHelpers.convexFunction2.is_convex())
        self.assertFalse(testHelpers.concaveFunction1.is_convex())
        self.assertFalse(testHelpers.concaveFunction2.is_convex())
        self.assertFalse(testHelpers.continuousFunction1.is_convex())
        self.assertFalse(testHelpers.continuousFunction2.is_convex())
        self.assertFalse(testHelpers.uppFunction1.is_convex())
        self.assertFalse(testHelpers.uppFunction2.is_convex())
        self.assertFalse(testHelpers.ultimatelyAffineFunction1.is_convex())
        self.assertFalse(testHelpers.ultimatelyAffineFunction1.is_convex())

    def test_is_ultimately_affine(self):
        self.assertTrue(testHelpers.ultimatelyAffineFunction1.is_ultimately_affine())
        self.assertTrue(testHelpers.ultimatelyAffineFunction1.is_ultimately_affine())
        self.assertTrue(testHelpers.convexFunction1.is_ultimately_affine())
        self.assertTrue(testHelpers.convexFunction2.is_ultimately_affine())
        self.assertTrue(testHelpers.concaveFunction1.is_ultimately_affine())
        self.assertTrue(testHelpers.concaveFunction2.is_ultimately_affine())
        self.assertFalse(testHelpers.continuousFunction1.is_ultimately_affine())
        self.assertFalse(testHelpers.continuousFunction2.is_ultimately_affine())
        self.assertFalse(testHelpers.uppFunction1.is_ultimately_affine())
        self.assertFalse(testHelpers.uppFunction2.is_ultimately_affine())


if __name__ == '__main__':
    unittest.main()
