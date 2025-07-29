
#
#
import argparse
import sys
#
import numpy as np
import matplotlib.pyplot as plt
from pybasics import read_file, write_file, info, warn
from pymol import cmd


def make_pdb(pdbname, x, data, name):

    pdb = read_file(pdbname, True)

    m = max(data)

    n_ccsp = [x / m * 100 for x in data]

    for _id, n in zip(x, n_ccsp):

        for i in range(len(pdb)):
            fields = pdb[i].split()

            if len(fields) > 1:
                if fields[2] == 'CA' and int(fields[5]) == _id:
                    bfactor = str(format(round(n, 2), '.2f'))
                    p1 = ''.join(pdb[i][:61]); p2 = ''.join(pdb[i][66:])
                    pdb[i] = p1 + ' ' + bfactor + p2
#                    pdb[i] = pdb[i].replace('0.00', bfactor)
                    break

    pdb = '\n'.join(pdb)

    pdbname = name + '_' + pdbname

    write_file(pdbname, pdb)

    info('comp2pse: %s written to disk!' % pdbname)

    return pdbname


def make_pse(pdbname, xna, xdis, xapp):

        cmd.load(pdbname)

        cmd.spectrum('b', 'white red')

        if len(xna) > 0:
            str_sel = 'resi ' + '+'.join(xna)
            cmd.select('NA', str_sel)
            cmd.color('black', 'NA')

        if len(xdis) > 0:
            str_sel = 'resi ' + '+'.join(xdis)
            cmd.select('DIS', str_sel)
            cmd.color('blue', 'DIS')

        if len(xapp) > 0:
            str_sel = 'resi ' + '+'.join(xapp)
            cmd.select('APP', str_sel)
            cmd.color('green', 'APP')

        psename = pdbname.split('.')[0] + '.pse'

        cmd.save(psename)

        cmd.delete('all')

        info('comp2pse: %s written to disk!' % psename)

        return None


def comp2pse(args):

    warn('Start: comp2pse')

    data = read_file(args.data, True)

    x = [int(x.split()[0]) for x in data]

    xna = [x.split()[0] for x in data if 'NA' in x]
    xdis = [x.split()[0] for x in data if 'DIS' in x]
    xapp = [x.split()[0] for x in data if 'APP' in x]

    data = '\n'.join(data)
    data = data.replace('NA', '0')
    data = data.replace('DIS', '0')
    data = data.replace('APP', '0')
    data = data.splitlines()

    ccsp = [float(x.split()[1]) for x in data]
    dH = [float(x.split()[2]) for x in data]
    dN = [float(x.split()[3]) for x in data]
    dI = [float(x.split()[4]) for x in data]

    pdbname = make_pdb(args.pdb, x, ccsp, 'ccsp')
    make_pse(pdbname, xna, xdis, xapp)

    pdbname = make_pdb(args.pdb, x, dH, 'dH')
    make_pse(pdbname, xna, xdis, xapp)

    pdbname = make_pdb(args.pdb, x, dN, 'dN')
    make_pse(pdbname, xna, xdis, xapp)

#    pdbname = make_pdb(args.pdb, x, dI, 'dI')
#    make_pse(pdbname, xna, xdis, xapp)

    warn('End: comp2pse')

    return None
