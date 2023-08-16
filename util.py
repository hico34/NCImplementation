from math import lcm, gcd
from fractions import Fraction


# Find the least common multiple of 2 fractions
def lcm_fraction(fr1, fr2):
    num = lcm(fr1.numerator, fr2.numerator)
    den = gcd(fr1.denominator, fr2.denominator)
    return Fraction(num, den)


def gcd_fraction(fr1, fr2):
    num = gcd(fr1.numerator, fr2.numerator)
    den = lcm(fr1.denominator, fr2.denominator)
    return Fraction(num, den)
