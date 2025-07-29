#
#
import argparse
import glob
import sys
import csv
import re
#
from pybasics import read_file, write_file, info, warn, AAS


def sub_ccpcsv2dat(peaklist):

    relevant_columns = ['Assign F1', 'Assign F2', 'Pos F1', 'Pos F2', 'Height']

    extracted_data = []

    with open(peaklist, newline='') as csvfile:
        peaks = csv.DictReader(csvfile)

        for row in peaks:
            # Extract only the relevant columns
            data = {col: row[col] for col in relevant_columns}

            # Optional: propagate assignment if only one is defined
            if data['Assign F1'] or data['Assign F2']:
                assign = data['Assign F1'] or data['Assign F2']
                data['Assign F1'] = data['Assign F2'] = assign

                del data['Assign F2']

                data['res_num'] = int(data['Assign F1'].split('.')[-3])
                data['res_type'] = data['Assign F1'].split('.')[-2]

                for aa in AAS:
                    if AAS[aa][1].upper() == data['res_type']:
                        data['res_type'] = aa

                del data['Assign F1']

                extracted_data.append(data)

    peaks = sorted(extracted_data, key=lambda x: x['res_num'])

    table = []

    for peak in peaks:

        table.append([peak['res_num'], peak['Pos F1'], peak['Pos F2'], peak['Height'], peak['res_type']])

    table = [' '.join([str(x) for x in s]) for s in table]

    table = '\n'.join(table)

    tname = peaklist.split('.')[0] + '.dat'

    write_file(tname, table)

    return None


def ccpcsv2dat(args):

    warn('Start: ccpcsv2dat')

    if type(args.input) == str:
        files = args.input.split()

    elif type(args.input) == bool:
        files = list(glob.glob('*.csv'))

    for peaklist in files:

        sub_ccpcsv2dat(peaklist)

        info('ccpcsv2dat: %s was converted!' % peaklist)

    warn('End: ccpcsv2dat')

    return None
