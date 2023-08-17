from helpers.util import lcm_fraction as lcm
from model.PiecewiseLinearFunction import PiecewiseLinearFunction


def convolution(f1: PiecewiseLinearFunction, f2: PiecewiseLinearFunction):
    period = lcm(f1.period, f2.period)
    increment = period * min(f1.periodic_slope, f2.periodic_slope)