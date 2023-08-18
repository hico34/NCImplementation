from fractions import Fraction
from model.Piece import Piece
from model.PiecewiseLinearFunction import PiecewiseLinearFunction

# Computes all x values where a segment start, and one x value in the middle of each segment
def relevant_x_values(f: PiecewiseLinearFunction):
    transient_x_values = []
    periodic_x_values = []
    for e in f.all_pieces:
        transient_x_values.append(e.x_start)
        x_within_segment = e.x_start + (e.x_end - e.x_start) / 2
        transient_x_values.append(x_within_segment)
        if e.x_start >= f.rank:
            periodic_x_values.append(e.x_start)
            periodic_x_values.append(x_within_segment)
    return transient_x_values, periodic_x_values




rank_continuous1 = Fraction(9.5)
period_continuous1 = Fraction(3.25)
increment_continuous1 = Fraction(5.75)
pieces_continuous1 = [
    Piece(Fraction(0), Fraction(0), Fraction(0), Fraction(3), Fraction(.5)),
    Piece(Fraction(3), Fraction(1.5), Fraction(1.5), Fraction(5), Fraction(1)),
    Piece(Fraction(5), Fraction(3.5), Fraction(3.5), Fraction(8), Fraction(4)),
    Piece(Fraction(8), Fraction(15.5), Fraction(15.5), Fraction(9.5), Fraction(.75)),
    Piece(Fraction(9.5), Fraction(16.625), Fraction(16.625), Fraction(12), Fraction(2)),
    Piece(Fraction(12), Fraction(21.625), Fraction(21.625), Fraction(12.75), Fraction(1))
]
rank_continuous2 = Fraction(11)
period_continuous2 = Fraction(10)
increment_continuous2 = Fraction(112, 5)
pieces_continuous2 = [
    Piece(Fraction(0), Fraction(1), Fraction(1), Fraction(2), Fraction(2)),
    Piece(Fraction(2), Fraction(4), Fraction(4), Fraction(7), Fraction(1.5)),
    Piece(Fraction(7), Fraction(11.5), Fraction(11.5), Fraction(10), Fraction(0.1)),
    Piece(Fraction(10), Fraction(59, 5), Fraction(59, 5), Fraction(11), Fraction(1)),
    Piece(Fraction(11), Fraction(64, 5), Fraction(64, 5), Fraction(14), Fraction(0)),
    Piece(Fraction(14), Fraction(64, 5), Fraction(64, 5), Fraction(21), Fraction(3.2))
]

rank_concave1 = Fraction(11)
period_concave1 = Fraction(1)
increment_concave1 = Fraction(0.5)
pieces_concave1 = [
    Piece(Fraction(0), Fraction(0), Fraction(1), Fraction(3), Fraction(4)),
    Piece(Fraction(3), Fraction(13), Fraction(13), Fraction(5), Fraction(3.5)),
    Piece(Fraction(5), Fraction(20), Fraction(20), Fraction(8), Fraction(2)),
    Piece(Fraction(8), Fraction(26), Fraction(26), Fraction(11), Fraction(1.25)),
    Piece(Fraction(11), Fraction(119, 4), Fraction(119, 4), Fraction(12), Fraction(0.5)),
]
rank_concave2 = Fraction(10)
period_concave2 = Fraction(1)
increment_concave2 = Fraction(1, 5)
pieces_concave2 = [
    Piece(Fraction(0), Fraction(0), Fraction(0), Fraction(4), Fraction(6)),
    Piece(Fraction(4), Fraction(24), Fraction(24), Fraction(7), Fraction(2)),
    Piece(Fraction(7), Fraction(30), Fraction(30), Fraction(8.5), Fraction(0.75)),
    Piece(Fraction(8.5), Fraction(31.125), Fraction(31.125), Fraction(10), Fraction(2, 5)),
    Piece(Fraction(10), Fraction(31.725), Fraction(31.725), Fraction(11), Fraction(1, 5)),
]

rank_convex1 = Fraction(12)
period_convex1 = Fraction(1)
increment_convex1 = Fraction(4.5)
pieces_convex1 = [
    Piece(Fraction(0), Fraction(0), Fraction(0), Fraction(4), Fraction(1)),
    Piece(Fraction(4), Fraction(4), Fraction(4), Fraction(6), Fraction(2)),
    Piece(Fraction(6), Fraction(8), Fraction(8), Fraction(6.5), Fraction(2.5)),
    Piece(Fraction(6.5), Fraction(9.25), Fraction(9.25), Fraction(12), Fraction(4)),
    Piece(Fraction(12), Fraction(31.25), Fraction(31.25), Fraction(13), Fraction(4.5)),
]
rank_convex2 = Fraction(8)
period_convex2 = Fraction(1)
increment_convex2 = Fraction(6)
pieces_convex2 = [
    Piece(Fraction(0), Fraction(2), Fraction(0), Fraction(2), Fraction(0.5)),
    Piece(Fraction(2), Fraction(1), Fraction(1), Fraction(5), Fraction(0.75)),
    Piece(Fraction(5), Fraction(3.25), Fraction(3.25), Fraction(6), Fraction(7, 5)),
    Piece(Fraction(6), Fraction(4.25), Fraction(4.25), Fraction(8), Fraction(5)),
    Piece(Fraction(8), Fraction(14.25), Fraction(14.25), Fraction(9), Fraction(6)),
]

rank_upp1 = Fraction(8)
period_upp1 = Fraction(3)
increment_upp1 = Fraction(7)
pieces_upp1 = [
    Piece(Fraction(0), Fraction(0), Fraction(0), Fraction(3), Fraction(.5)),
    Piece(Fraction(3), Fraction(1.5), Fraction(1.5), Fraction(5), Fraction(17, 10)),
    Piece(Fraction(5), Fraction(7), Fraction(6), Fraction(8), Fraction(2, 5)),
    Piece(Fraction(8), Fraction(37, 5), Fraction(37, 5), Fraction(9), Fraction(1)),
    Piece(Fraction(9), Fraction(11.5), Fraction(11.5), Fraction(11), Fraction(3))
]

rank_upp2 = Fraction(9)
period_upp2 = Fraction(5)
increment_upp2 = Fraction(8)
pieces_upp2 = [
    Piece(Fraction(0), Fraction(0), Fraction(0), Fraction(3), Fraction(1)),
    Piece(Fraction(3), Fraction(1.5), Fraction(1.5), Fraction(5), Fraction(2.5)),
    Piece(Fraction(5), Fraction(7), Fraction(3.5), Fraction(9), Fraction(1, 5)),
    Piece(Fraction(9), Fraction(9.5), Fraction(10.5), Fraction(10), Fraction(4)),
    Piece(Fraction(10), Fraction(12.5), Fraction(11.5), Fraction(14), Fraction(1))
]

# Provide functions for tests
concaveFunction1 = PiecewiseLinearFunction(pieces_concave1, rank_concave1, period_concave1, increment_concave1)
concaveFunction2 = PiecewiseLinearFunction(pieces_concave2, rank_concave2, period_concave2, increment_concave2)
convexFunction1 = PiecewiseLinearFunction(pieces_convex1, rank_convex1, period_convex1, increment_convex1)
convexFunction2 = PiecewiseLinearFunction(pieces_convex2, rank_convex2, period_convex2, increment_convex2)
continuousFunction1 = PiecewiseLinearFunction(pieces_continuous1, rank_continuous1, period_continuous1, increment_continuous1)
continuousFunction2 = PiecewiseLinearFunction(pieces_continuous2, rank_continuous2, period_continuous2, increment_continuous2)
finiteFunction1 = None
finiteFunction2 = None
ultimatelyAffineFunction1 = None
ultimatelyAffineFunction2 = None
uppFunction1 = PiecewiseLinearFunction(pieces_upp1, rank_upp1, period_upp1, increment_upp1)
uppFunction2 = PiecewiseLinearFunction(pieces_upp2, rank_upp2, period_upp2, increment_upp2)

test_functions = [concaveFunction1, concaveFunction2, convexFunction1, convexFunction2, continuousFunction1, continuousFunction2, uppFunction1, uppFunction2]


