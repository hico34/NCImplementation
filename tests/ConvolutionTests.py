import unittest
from model.Piece import Piece
from model.PiecewiseLinearFunction import PiecewiseLinearFunction
from fractions import Fraction
from operations.Convolution import convolution

class ConvolutionTests(unittest.TestCase):

    e1 = [
        Piece(Fraction(0), Fraction(0), Fraction(3), Fraction(2), Fraction(1)),
        Piece(Fraction(2), Fraction(5), Fraction(5), Fraction(4), Fraction(0)),
        Piece(Fraction(4), Fraction(5), Fraction(5), Fraction(2), Fraction(1))
    ]
    f1 = PiecewiseLinearFunction(e1, Fraction(2), Fraction(4), Fraction(2))
    e2 = [
        Piece(Fraction(0), Fraction(0), Fraction(0), Fraction(2), Fraction(2)),
        Piece(Fraction(2), Fraction(4), Fraction(4), Fraction(4), Fraction(0)),
        Piece(Fraction(5), Fraction(4), Fraction(4), Fraction(2), Fraction(3))
    ]
    f2 = PiecewiseLinearFunction(e2, Fraction(2), Fraction(4), Fraction(3))

    def test_convolution(self):
        convolution(self.f1, self.f2)

if __name__ == '__main__':
    unittest.main()