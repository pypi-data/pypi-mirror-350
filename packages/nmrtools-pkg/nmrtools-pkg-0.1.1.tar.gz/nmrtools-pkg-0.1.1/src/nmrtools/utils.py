#
#
import numpy as np
from pybasics import sumd, multid


DINT = 20000000

def dX(reference, target, n=None):
    """.
    """
    if n == 'N':
        DPPM = 0.12
    else:
        DPPM = 0.02

    dX, ddX = sumd(-1 * float(reference), DPPM, float(target), DPPM)

    return dX, ddX


def rX(reference, target):
    """.
    """
    rX, drX = multid(float(target), DINT, 1 / float(reference), 0)

    return rX, drX


def csp(dH, ddH, dN, ddN):
    """.
    """

    _dH, _ddH = multid(dH, ddH, dH, ddH)
    _dN, _ddN = multid(dN, ddN, dN, ddN)

    _dN = 1/6 * _dN
    _ddN = 1/6 * _ddN

    _ccsp, _dccsp = sumd(_dH, _ddH, _dN, _ddN)

    ccsp = np.sqrt(_ccsp)
    dccsp = _dccsp / 2

    return ccsp, dccsp
