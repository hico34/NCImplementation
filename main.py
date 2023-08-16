import sys

sys.path.insert(0, 'C:/Users/Philip/Documents/Retro/NCImplementation/model')
sys.path.insert(0, 'C:/Users/Philip/Documents/Retro/NCImplementation/operations')
sys.path.insert(0, 'C:/Users/Philip/Documents/Retro/NCImplementation/util')

from model.PiecewiseLinearFunction import PiecewiseLinearFunction
from model.Element import Element
from fractions import Fraction
from helpers.util import lcm_fraction as lcm
import numpy as np2

elementList = [
    Element(Fraction(0), Fraction(0), Fraction(0), Fraction(3), Fraction(.5)),
    Element(Fraction(3), Fraction(1.5), Fraction(1.5), Fraction(5), Fraction(1)),
    Element(Fraction(5), Fraction(7), Fraction(3.5), Fraction(8), Fraction(1.5)),
    Element(Fraction(8), Fraction(10.5), Fraction(10.5), Fraction(9), Fraction(1)),
    Element(Fraction(9), Fraction(11.5), Fraction(11.5), Fraction(11), Fraction(2))
]



elementList2 = [
    Element(Fraction(0), Fraction(0), Fraction(0), Fraction(3), Fraction(.5)),
    Element(Fraction(3), Fraction(1.5), Fraction(1.5), Fraction(5), Fraction(1)),
    Element(Fraction(5), Fraction(7), Fraction(3.5), Fraction(8), Fraction(1.5)),
    Element(Fraction(8), Fraction(10.5), Fraction(10.5), Fraction(10), Fraction(2)),
    Element(Fraction(10), Fraction(12.5), Fraction(11.5), Fraction(14), Fraction(4))
]

plf = PiecewiseLinearFunction(elementList, Fraction(8), Fraction(3), Fraction(5))
plf2 = PiecewiseLinearFunction(elementList2, Fraction(8), Fraction(6), Fraction(20))

fr1 = Fraction(4, 2)
fr2 = Fraction(7,2)
print(lcm(fr1, fr2))

#result = min_of_plfs(plf, plf2)
print("Result: ")
#print(result)

x = np2.array([Fraction(0), Fraction(1), Fraction(3), Fraction(4), Fraction(5), Fraction(20)])
print(plf.numpy_values_at(x))
print([plf.value_at(Fraction(0)), plf.value_at(Fraction(1)), plf.value_at(Fraction(3)), plf.value_at(Fraction(4)), plf.value_at(Fraction(5)), plf.value_at(Fraction(20))])