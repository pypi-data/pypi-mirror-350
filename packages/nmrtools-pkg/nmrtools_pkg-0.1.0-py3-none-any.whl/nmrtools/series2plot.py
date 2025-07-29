#
#
import argparse
import glob
import re
import sys
import os
#
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
from scipy.optimize import curve_fit
from pybasics import read_file, write_file, info, warn
from fpdf import FPDF
from PIL import Image



def kd(x, a, b):

    y = (a * x) / (b + x)

    return y

def alphanum_key(s):
    # Split into digit and non-digit parts
    return [int(part) if part.isdigit() else part for part in re.split(r'(\d+)', s)]


def series2plot(args):

    warn('Start: series2plot')

    output_names = []

    for fname in glob.glob(os.path.join(args.input, '*.dat')):

        data = read_file(fname, True)[1:]

        x = np.array([float(x.split()[0]) for x in data])
        H = np.array([float(x.split()[1]) for x in data])
        N = np.array([float(x.split()[2]) for x in data])
        I = np.array([float(x.split()[3]) for x in data])

        dH = H - H[0]
        dN = N - N[0]
        dI = I / I[0]
        ccsp = np.sqrt(dH**2 + 1/6*dN**2)

        f_x = np.linspace(0, np.max(x), 100)

        # using the variable axs for multiple Axes
        fig, axes = plt.subplots(2, 2, figsize=(8, 6))

        try:
            popt, pcov = curve_fit(kd, x, dH)
            pcov = np.sqrt(np.diag(pcov))
            f_dH = kd(f_x, *popt)
        except:
            popt = [0, 0]
            pcov = [0, 0]

        axes[0, 0].plot(x, dH, color='salmon', label='dH')
        if popt[1] > pcov[1]:
            axes[0, 0].plot(f_x, f_dH, color='grey', label='fit: kD=%5.3f +/- %5.3f' % (popt[1], pcov[1]))
        axes[0, 0].set_xlabel('Ligand (µM)')
        axes[0, 0].set_ylabel('dH')
        axes[0, 0].ticklabel_format(useOffset=False)
        axes[0, 0].legend()

        try:
            popt, pcov = curve_fit(kd, x, dN)
            pcov = np.sqrt(np.diag(pcov))
            f_dN = kd(f_x, *popt)
        except:
            popt = [0, 0]
            pcov = [0, 0]

        axes[0, 1].plot(x, dN, color='salmon', label='dN')
        if popt[1] > pcov[1]:
            axes[0, 1].plot(f_x, f_dN, color='grey', label='fit: kD=%5.3f +/- %5.3f' % (popt[1], pcov[1]))
        axes[0, 1].set_xlabel('Ligand (µM)')
        axes[0, 1].set_ylabel('dN')
        axes[0, 1].ticklabel_format(useOffset=False)
        axes[0, 1].legend()

        try:
            popt, pcov = curve_fit(kd, x, dI)
            pcov = np.sqrt(np.diag(pcov))
            f_dI = kd(f_x, *popt)
        except:
            popt = [0, 0]
            pcov = [0, 0]

        axes[1, 0].plot(x, dI, color='salmon', label='dI')
        if popt[1] > pcov[1]:
            axes[1, 0].plot(f_x, f_dI, color='grey', label='fit: kD=%5.3f +/- %5.3f' % (popt[1], pcov[1]))
        axes[1, 0].set_xlabel('Ligand (µM)')
        axes[1, 0].set_ylabel('dI')
        axes[1, 0].ticklabel_format(useOffset=False, style='plain')
        axes[1, 0].legend()

        try:
            popt, pcov = curve_fit(kd, x, ccsp)
            pcov = np.sqrt(np.diag(pcov))
            f_ccsp = kd(f_x, *popt)
        except:
            popt = [0, 0]
            pcov = [0, 0]

        axes[1, 1].plot(x, ccsp, color='salmon', label='CCSP')
        if popt[1] > pcov[1]:
            axes[1, 1].plot(f_x, f_ccsp, color='grey', label='fit: kD=%5.3f +/- %5.3f' % (popt[1], pcov[1]))
        axes[1, 1].set_xlabel('Ligand (µM)')
        axes[1, 1].set_ylabel('CCSP')
        axes[1, 1].ticklabel_format(useOffset=False)
        axes[1, 1].legend()

        fig.suptitle(fname)

        if args.output:
            oname = args.output.split('.')[0]
        else:
            oname = fname.split('.')[0]

        plt.tight_layout()

        plt.savefig(oname + '.eps', bbox_inches='tight', dpi=600)
        info('series2plot: %s.eps saved on disk!' % oname)

        plt.savefig(oname + '.png', bbox_inches='tight', dpi=600)
        info('series2plot: %s.png saved on disk!' % oname)

        info('series2plot: showing %s' % oname)

        output_names.append(oname + '.png')

        if args.show == 'True':
            plt.show()

        plt.close()

    output_names = sorted(output_names, key=alphanum_key)

    # Open the first image and convert to RGB (required for PDF)
    first_image = Image.open(output_names[0]).convert('RGB')

    # Convert remaining images and store them in a list
    image_list = [Image.open(f).convert('RGB') for f in output_names[1:]]

    # Save all images to a single PDF
    first_image.save('series2plot.pdf', save_all=True, append_images=image_list)

    warn('End: series2plot')

    return None
