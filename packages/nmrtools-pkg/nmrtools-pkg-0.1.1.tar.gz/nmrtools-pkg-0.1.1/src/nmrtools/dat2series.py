#
#
import argparse
import shutil
import sys
import os
#
import numpy as np
from pybasics import read_file, write_file, info, warn


def dat2series(args):

    warn('Start: dat2series')

    lst = read_file(args.input, True)

    files = [x.split()[0] for x in lst]

    if len(lst[0].split()) == 2:
        xaxis = [float(x.split()[1]) * args.concentration for x in lst]
    else:
        xaxis = [i for i in range(len(files))]

    if args.output:
        oname = args.output
    else:
        oname = 'resi'

    if os.path.exists(oname):
        shutil.rmtree(oname)

    os.mkdir(oname)

    series = {}

    for fname in files:
        data = read_file(fname, True)

        for line in data:
            aa, H, N, I, T = line.split()

            series[aa] = {
                'x': xaxis,
                'H': [0 for f in files],
                'N': [0 for f in files],
                'I': [0 for f in files],
                'T': T
            }

    for i, fname in enumerate(files):
        data = read_file(fname, True)

        for line in data:
            aa, H, N, I, T = line.split()

            series[aa]['H'][i] = H
            series[aa]['N'][i] = N
            series[aa]['I'][i] = I

    for aa in series.keys():
        data = ['x H N I']

        for x, h, n, i in zip(xaxis, series[aa]['H'], series[aa]['N'], series[aa]['I']):
            data.append(' '.join([str(x), str(h), str(n), str(i)]))

        data = '\n'.join(data)

        resname = os.path.join(oname, str(aa) + series[aa]['T'] + '.dat')

        write_file(resname, data)

    warn('End: dat2series')

    return None
