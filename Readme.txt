A short overview: 
Data structures are in package model, operations are in package operations, and tests are in package tests.

To try out this implementation, you may start the python interpreter within the top level directory (the one containing this file), and run the following code snippet:

from model.PiecewiseLinearFunction import PiecewiseLinearFunction
from model.Piece import Piece

f1_example = PiecewiseLinearFunction([
    Piece(0, 0, 0, 1, 1),
    Piece(1, 1, 1, 2, 0),
    Piece(2, 1, 1, 4, 2)
], 1, 3, 4)
f2_example = PiecewiseLinearFunction([
    Piece(0, 1, 1, 2, 0),
    Piece(2, 1, 1, 4, 1),
    Piece(4, 3, 3, 5, 0)
], 2, 3, 2)

These are the example functions on which the convolution is demonstrated in chapter 4.

To try out the operations, choose the modules you need and import them with the following code:
from operations.Maximum import maximum
from operations.Minimum import minimum
from operations.Addition import add_functions
from operations.Subtraction import subtract_functions
from operations.Convolution import convolution
from operations.MaxPlusConvolution import maxplus_convolution

PiecewiseLinearFunction has a __str__ method that shows the representation of the function if you want to print it.


To run tests, run the following command within the top level directory:
python -m tests.$TESTNAME

Please note that the FunctionTests require numpy to be installed.