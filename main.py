from Element import Element
from PiecewiseLinearFunction import PiecewiseLinearFunction
from AdditionSubtraction import add_plfs

elementList = [
    Element(0, 0, 0, 3, .5),
    Element(3, 1.5, 1.5, 5, 1),
    Element(5, 7, 3.5, 8, 1.5),
    Element(8, 10.5, 10.5, 9, 1),
    Element(9, 11.5, 11.5, 11, 2)
]

plf = PiecewiseLinearFunction(elementList, 8, 3, 5)
plf2 = PiecewiseLinearFunction(elementList, 8, 3, 5)

result = add_plfs(plf, plf2)
print("Result: ")
print(result)
