#
#
import argparse
import sys
#
import numpy as np
import matplotlib.pyplot as plt
import matplotlib
import matplotlib.patches as mpatches
from pybasics import read_file, write_file, info, warn


def comp2plot(args):

    warn('Start: comp2plot')

    flags = args.plot.split(',')

    value = True if 'value' in flags else False
    app = True if 'app' in flags else False
    dis = True if 'dis' in flags else False
    nd = True if 'nd' in flags else False

    rdata = read_file(args.data)

    data = rdata
    data = data.replace('NA', '0')
    data = data.replace('DIS', '0')
    data = data.replace('APP', '0')

    data = data.splitlines()

    xaxis = [int(x.split()[0]) for x in data]

    ccsp = [float(x.split()[1]) for x in data]
    dH = [float(x.split()[2]) for x in data]
    dN = [float(x.split()[3]) for x in data]
    dI = [float(x.split()[4]) for x in data]

    dccsp = [float(x.split()[5]) for x in data]
    ddH = [float(x.split()[6]) for x in data]
    ddN = [float(x.split()[7]) for x in data]
    ddI = [float(x.split()[8]) for x in data]

    rT = [x.split()[-1] for x in data]

    xna = [int(x.split()[0]) for x in rdata.splitlines() if 'NA' in x]
    xdis = [int(x.split()[0]) for x in rdata.splitlines() if 'DIS' in x]
    xapp = [int(x.split()[0]) for x in rdata.splitlines() if 'APP' in x]

    # using the variable axs for multiple Axes
    fig, axes = plt.subplots(2, 2, figsize=(8, 6))

    if value: axes[0, 0].bar(xaxis, ccsp, color='salmon', label='ccsp')
 #   axes[0, 0].errorbar(xaxis, ccsp, yerr=dccsp, fmt='none', color='grey')
    axes[0, 0].set_xlabel('Residues')
    axes[0, 0].set_ylabel('CCSP')

    if value: axes[0, 1].bar(xaxis, dI, color='salmon', label='dI')
 #   axes[0, 1].errorbar(xaxis, dI, yerr=ddI, fmt='none', color='grey')
    axes[0, 1].set_xlabel('Residues')
    axes[0, 1].set_ylabel('dI')

    if value: axes[1, 0].bar(xaxis, dH, color='salmon', label='dH')
 #   axes[1, 0].errorbar(xaxis, dH, yerr=ddH, fmt='none', color='grey')
    axes[1, 0].set_xlabel('Residues')
    axes[1, 0].set_ylabel('dH')

    if value: axes[1, 1].bar(xaxis, dN, color='salmon', label='dN')
  #  axes[1, 1].errorbar(xaxis, dN, yerr=ddN, fmt='none', color='grey')
    axes[1, 1].set_xlabel('Residues')
    axes[1, 1].set_ylabel('dN')

    for x in xna:
        for i in range(axes.shape[0]):
            for j in range(axes.shape[1]):
                if nd:
                    axes[i, j].axvline(x, color='lightgrey', linewidth=0.2)

    for x in xdis:
        for i in range(axes.shape[0]):
            for j in range(axes.shape[1]):
                if dis:
                    axes[i, j].axvline(x, color='blue', linewidth=0.2)

    for x in xapp:
        for i in range(axes.shape[0]):
            for j in range(axes.shape[1]):
                if app:
                    axes[i, j].axvline(x, color='green', linewidth=0.2)

    fig.suptitle(args.data)

    if args.output:
        oname = args.output.split('.')[0]
    else:
        oname = args.data.split('.')[0]

    plt.tight_layout()

    plt.rcParams['svg.fonttype'] = 'none'
    matplotlib.rcParams['pdf.fonttype'] = 42
    matplotlib.rcParams['ps.fonttype'] = 42

    plt.savefig(oname + '.eps', bbox_inches='tight')
    info('comp2plot: %s.eps saved on disk!' % oname)

    plt.savefig(oname + '.png', bbox_inches='tight')
    info('comp2plot: %s.png saved on disk!' % oname)

    plt.savefig(oname + '.pdf', bbox_inches='tight')
    info('comp2plot: %s.pdf saved on disk!' % oname)

    plt.savefig(oname + '.svg', bbox_inches='tight')
    info('comp2plot: %s.svg saved on disk!' % oname)

    info('comp2plot: showing %s' % oname)
    plt.show()

    plt.close()

    warn('End: comp2plot')

    return None
