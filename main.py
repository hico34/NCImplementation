import sys

sys.path.insert(0, 'C:/Users/Philip/Documents/Retro/NCImplementation/model')
sys.path.insert(0, 'C:/Users/Philip/Documents/Retro/NCImplementation/operations')
sys.path.insert(0, 'C:/Users/Philip/Documents/Retro/NCImplementation/util')

from model.PiecewiseLinearFunction import PiecewiseLinearFunction
from model.Piece import Piece
from operations.Maximum import maximum
from operations.Minimum import minimum
from operations.Addition import add_functions
from operations.Subtraction import subtract_functions
from operations.Convolution import convolution
from operations.MaxPlusConvolution import maxplus_convolution


f1_example = PiecewiseLinearFunction([
    Piece(0, 0, 0, 1, 1),
    Piece(1, 1, 1, 2, 0),
    Piece(2, 1, 1, 4, 2)
], 1, 3, 4)

f2_example = PiecewiseLinearFunction([
    Piece(0, 1, 1, 2, 0),
    Piece(2, 1, 1, 4, 1),
    Piece(4, 3, 3, 5, 0)
])
