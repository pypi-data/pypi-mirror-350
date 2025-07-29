#
#
import argparse
import glob
import sys
#
from pybasics import read_file, write_file, info, warn


def sub_peaks2dat(peaklist):

    peaks = read_file(peaklist, True)

    table = []

    for i, line in enumerate(peaks):
        if line[0] != '#':
            break
        else:
            peaks[i] = str()

    peaks = [x for x in peaks if x]

    for i in range(0, len(peaks), 2):
        cline = peaks[i].split()
        nline = peaks[i + 1].split()

        line = [int(nline[-1][1:]), cline[1], cline[2], cline[5], nline[-1][0]]

        table.append(line)

    table = sorted(table)

    table = [' '.join([str(x) for x in s]) for s in table]

    table = '\n'.join(table)

    tname = peaklist.split('.')[0] + '.dat'

    write_file(tname, table)

    return None


def peaks2dat(args):

    warn('Start: peaks2dat')

    if type(args.input) == str:
        files = args.input.split()

    elif type(args.input) == bool:
        files = list(glob.glob('*.peaks'))

    for peaklist in files:

        sub_peaks2dat(peaklist)

        info('peaks2dat: %s was converted!' % peaklist)

    warn('End: peaks2dat')

    return None
