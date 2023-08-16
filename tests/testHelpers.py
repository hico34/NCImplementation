from fractions import Fraction
from model.Element import Element
from model.PiecewiseLinearFunction import PiecewiseLinearFunction

# Computes all x values where a segment start, and one x value in the middle of each segment
def relevant_x_values(f):
    transient_x_values = []
    periodic_x_values = []
    for e in f.all_elements:
        transient_x_values.append(e.x_start)
        x_within_segment = e.x_start + (e.x_end - e.x_start) / 2
        transient_x_values.append(x_within_segment)
        if e.x_start >= f.rank:
            periodic_x_values.append(e.x_start)
            periodic_x_values.append(x_within_segment)
    return transient_x_values, periodic_x_values




rank_continous1 = Fraction(9.5)
period_continous1 = Fraction(3.25)
increment_continous1 = Fraction(5.75)
elements_continous1 = [
    Element(Fraction(0), Fraction(0), Fraction(0), Fraction(3), Fraction(.5)),
    Element(Fraction(3), Fraction(1.5), Fraction(1.5), Fraction(5), Fraction(1)),
    Element(Fraction(5), Fraction(3.5), Fraction(3.5), Fraction(8), Fraction(4)),
    Element(Fraction(8), Fraction(15.5), Fraction(15.5), Fraction(9.5), Fraction(.75)),
    Element(Fraction(9.5), Fraction(16.625), Fraction(16.625), Fraction(12), Fraction(2)),
    Element(Fraction(12), Fraction(21.625), Fraction(21.625), Fraction(12.75), Fraction(1))
]
rank_continous2 = Fraction(11)
period_continous2 = Fraction(10)
increment_continous2 = Fraction(22.4)
elements_continous2 = [
    Element(Fraction(0), Fraction(1), Fraction(1), Fraction(2), Fraction(2)),
    Element(Fraction(2), Fraction(4), Fraction(4), Fraction(7), Fraction(1.5)),
    Element(Fraction(7), Fraction(11.5), Fraction(11.5), Fraction(10), Fraction(0.1)),
    Element(Fraction(10), Fraction(11.8), Fraction(11.8), Fraction(11), Fraction(1)),
    Element(Fraction(11), Fraction(12.8), Fraction(12.8), Fraction(14), Fraction(0)),
    Element(Fraction(14), Fraction(12.8), Fraction(12.8), Fraction(21), Fraction(3.2))
]
elements_continous3 = [
    Element(Fraction(0), Fraction(1), Fraction(1), Fraction(2), Fraction(2)),
    Element(Fraction(2), Fraction(3), Fraction(3), Fraction(7), Fraction(1.5)),
    Element(Fraction(7), Fraction(12), Fraction(12), Fraction(10), Fraction(0.1)),
    Element(Fraction(10), Fraction(12.8), Fraction(12.8), Fraction(11), Fraction(1)),
    Element(Fraction(11), Fraction(13.8), Fraction(13.8), Fraction(14), Fraction(0)),
    Element(Fraction(14), Fraction(25.8), Fraction(25.8), Fraction(21), Fraction(3.2))
]

elements_concave1 = []
elements_concave2 = []

elements_convex1 = []
elements_convex2 = []

rank_upp1 = Fraction(8)
period_upp1 = Fraction(3)
increment_upp1 = Fraction(7)
elements_upp1 = [
    Element(Fraction(0), Fraction(0), Fraction(0), Fraction(3), Fraction(.5)),
    Element(Fraction(3), Fraction(1.5), Fraction(1.5), Fraction(5), Fraction(1.7)),
    Element(Fraction(5), Fraction(7), Fraction(6), Fraction(8), Fraction(0.4)),
    Element(Fraction(8), Fraction(7.2), Fraction(7.2), Fraction(9), Fraction(1)),
    Element(Fraction(9), Fraction(11.5), Fraction(11.5), Fraction(11), Fraction(3))
]

rank_upp2 = Fraction(9)
period_upp2 = Fraction(5)
increment_upp2 = Fraction(8)
elements_upp2 = [
    Element(Fraction(0), Fraction(0), Fraction(0), Fraction(3), Fraction(1)),
    Element(Fraction(3), Fraction(1.5), Fraction(1.5), Fraction(5), Fraction(2.5)),
    Element(Fraction(5), Fraction(7), Fraction(3.5), Fraction(9), Fraction(0.2)),
    Element(Fraction(9), Fraction(9.5), Fraction(10.5), Fraction(10), Fraction(4)),
    Element(Fraction(10), Fraction(12.5), Fraction(11.5), Fraction(14), Fraction(1))
]

# Provide functions for tests
concaveFunction1 = None
concaveFunction2 = None
convexFunction1 = None
concaveFunction2 = None
continousFunction1 = PiecewiseLinearFunction(elements_continous1, rank_continous1, period_continous1, increment_continous1)
continousFunction2 = PiecewiseLinearFunction(elements_continous2, rank_continous2, period_continous2, increment_continous2)
finiteFunction1 = None
finiteFunction2 = None
ultimatelyAffineFunction1 = None
ultimatelyAffineFunction2 = None
uppFunction1 = PiecewiseLinearFunction(elements_upp1, rank_upp1, period_upp1, increment_upp1)
uppFunction2 = PiecewiseLinearFunction(elements_upp2, rank_upp2, period_upp2, increment_upp2)


