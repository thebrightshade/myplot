import pandas as pd
import numpy as np
import sys
import plotly
import argparse


def main():
    args = parseargs()
    df = create_df(args)
    scan_list = create_list_from_df(df, 'Scan')
    scan = split_list(scan_list)
    print(scan)
    print('SCAN >>>>>>>>>', type(scan))


def parseargs():
    parser = argparse.ArgumentParser()
    parser.add_argument('--file')

    args = parser.parse_args()

    return args


def create_df(args):
    df = pd.read_csv(args.file, header=None, names=[
                     'Time', 'Iteration', 'Test Case', 'Result',
                     'Scan', 'Connect', 'Pair', ''])
    return df


def create_list_from_df(dataframe, column):
    my_list = dataframe[column].tolist()
    return my_list


def split_list(my_list):
    new_list = []
    for index, item in enumerate(my_list):
        new_item = str(item).split()
        if len(new_item) > 1:
            new_list.append(new_item[-2])
            print(new_item[-2])
        # else:
        #     del my_list[index]

    return new_list


if __name__ == "__main__":
    main()
