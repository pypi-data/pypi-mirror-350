#
#
import argparse
import sys
#
import numpy as np
from pybasics import read_file, write_file, info, warn
#
from nmrtools.utils import dX, rX, csp


class Protein:

    def __init__(self):

        self.residues = []

        return None

    def append(self, residue):

        self.residues.append(residue)

        return None


class Residue:

    def __init__(self, _id):

        self.id = _id

        self.r = False
        self.t = False

        return None

def dat2comp(args):

    warn('Start: dat2comp')

    rname = args.reference.split('.')[0]
    tname = args.target.split('.')[0]

    if args.output:
        oname = args.output.split('.')[0]
    else:
        oname = 'd2D_' + rname + '_x_' + tname

    reference = read_file(args.reference, True)
    test = read_file(args.target, True)

    rids = [int(x.split()[0]) for x in reference]
    tids = [int(x.split()[0]) for x in test]

    ids = rids + tids

    ids = [i for i in range(min(ids), max(ids) + 1)]

    protein = Protein()

    for _id in ids:
        res = Residue(_id)

        if _id in rids:
            res.r = True

        if _id in tids:
            res.t = True

        if res.r and res.t:
            r = reference[rids.index(_id)]
            t = test[tids.index(_id)]

            rH, rN, rI, rT = r.split()[1:]
            tH, tN, tI, tT = t.split()[1:]

            dH, ddH = dX(rH, tH, n='H')
            dN, ddN = dX(rN, tN, n='N')

            ccsp, dccsp = csp(dH, ddH, dN, ddN)

            try:
                dI, ddI = rX(rI, tI)
            except:
                dI = ddI = 'NA'

            res.dH, res.dN, res.ccsp, res.dI, res.T = dH, dN, ccsp, dI, rT
            res.ddH, res.ddN, res.dccsp, res.ddI = ddH, ddN, dccsp, ddI

            res.data = ' '.join(
                    [
                        str(_id),
                        str(ccsp),
                        str(dH),
                        str(dN),
                        str(dI),
                        str(dccsp),
                        str(ddH),
                        str(ddN),
                        str(ddI),
                        str(rT)
                ]
            )

        elif res.r and not res.t:

            rH, rN, rI, rT = reference[rids.index(_id)].split()[1:]

            res.data = ' '.join(
                    [
                        str(_id),
                        'DIS',
                        'DIS',
                        'DIS',
                        'DIS',
                        'DIS',
                        'DIS',
                        'DIS',
                        'DIS',
                        str(rT)
                ]
            )

        elif not res.r and res.t:

            tH, tN, tI, tT = test[tids.index(_id)].split()[1:]

            res.data = ' '.join(
                    [
                        str(_id),
                        'APP',
                        'APP',
                        'APP',
                        'APP',
                        'APP',
                        'APP',
                        'APP',
                        'APP',
                        str(tT)
                ]
            )
        elif not res.r and not res.t:
            res.data = ' '.join(
                    [
                        str(_id),
                        'NA',
                        'NA',
                        'NA',
                        'NA',
                        'NA',
                        'NA',
                        'NA',
                        'NA',
                        'NA'
                ]
            )
        protein.append(res)

        data = '\n'.join([res.data for res in protein.residues])

    write_file(oname + '.dat', data)

    info('dat2comp: %s was processed!' % oname)

    warn('End: dat2comp')

    return None
