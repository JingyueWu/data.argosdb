#!/usr/bin/env python
# -*- coding: utf-8 -*-

import csv
import argparse
import sys
import os
__version__ = "1.0.0"
__status__ = "Production"


def usr_args():
    """Program Arguments
    Arguments for process are defined here.
    """

    # initialize parser
    parser = argparse.ArgumentParser()

    # set usages options
    parser = argparse.ArgumentParser(
        prog='transform_hive_qc.py',
        usage='%(prog)s [options]')

    # version
    parser.add_argument(
        '-v', '--version',
        action='version',
        version='%(prog)s ' + __version__)

    parser.add_argument('-f', '--file',
        required=True,
        help="Input file. The input file should be a QC CSV file from HIVE.")
    parser.add_argument('-o', '--output',
        help="Output file. If no output is provided, the resulting CSV will \
            be directed to the terminal.")
    if len(sys.argv) <= 1:
        sys.argv.append('--help')

    return parser.parse_args()


def transform_csv(csv_file_name, mapping, output_file_name):
    """transform_csv
    Transform HIVE QC output csv to ARGOS tsv format

    Parameters
    ----------
    csv_file_name: str
        file path/name to HIVE QC CSV
    output: str, optional
        file path/name to direct data to
    """
    csv_file = open(csv_file_name)
    csv_reader = csv.reader(csv_file, delimiter=',', \
                            skipinitialspace=True)
    if output_file_name:
        output_file_path = os.path.abspath(output_file_name)
        output_file = open(output_file_path, 'w', encoding='utf8')
        writer = csv.writer(output_file, delimiter='\t')
    # Get a list of indexes of the columns we want to keep
    line_count = 0
    for row in csv_reader:
        if line_count == 0:  # First row
            # print(f'Column names are {row}')
            line_count += 1
            index_list = [row.index(varname) for varname in mapping.keys() \
                          if varname in row]
            var_list = [mapping[varname] for varname in mapping.keys() \
                        if varname in row]
            # print(f'index list is: {index_list}')
            if output_file_name:
                writer.writerow(var_list)
            else:
                print(f'{",".join(var_list)}')
        else:
            row_out = [row[i] for i in index_list]
            if output_file_name:
                writer.writerow(row_out)
            else:
                print(f'{",".join(row_out)}')
            line_count += 1
    

def main():
    """
    Main function
    """
    args = usr_args()
    var_mapping = {'FileName': 'file_name',
                   'qA': 'avg_quality_a',
                   'qC': 'avg_quality_c',
                   'qG': 'avg_quality_g',
                   'qT': 'avg_quality_T',
                   'Avg File Qual': 'avg_file_quality',
                   'Position Outlier Count': 'pos_outlier_count',
                   'Num Reads': 'num_reads',
                   'min Read Length': 'min_read_length',
                   'avg Read Length': 'avg_read_length',
                   'min Read Length': 'min_read_length',
                   'max Read Length': 'max_read_length',
                   'gc Content': 'gc_cont'}
    transform_csv(args.file, var_mapping, args.output)

#______________________________________________________________________________#
if __name__ == "__main__":
    main()
