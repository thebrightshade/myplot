import pandas as pd
import numpy as np
import sys
import plotly.graph_objs as go
import argparse


def parseargs():
    parser = argparse.ArgumentParser()
    parser.add_argument('--file')

    args = parser.parse_args(None if sys.argv[1:] else ['-h'])

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
        # else:
        #     del my_list[index]

    return new_list


def main():
    args = parseargs()
    df = create_df(args)
    scan_list = create_list_from_df(df, 'Scan')
    scan = split_list(scan_list)
    connect_list = create_list_from_df(df, 'Connect')
    connect = split_list(connect_list)
    pair_list = create_list_from_df(df, 'Pair')
    pair = split_list(pair_list)
    # print(scan)
    print('SCAN >>>>>>>>> {}, Number of values: {}'.format(
        type(scan), len(scan)))
    print('CONNECT >>>>>>>>> {}, Number of values: {}'.format(
        type(connect), len(connect)))
    print('PAIR >>>>>>>>> {}, Number of values: {}'.format(
        type(pair), len(pair)))
    fig = go.FigureWidget()
    fig.add_bar(x=[a for a, b in enumerate(scan)],
                y=scan,
                marker={'color': 'orange',
                        'opacity': 0.8,
                        },
                showlegend=True,
                name='Scan')
    fig.add_bar(x=[a for a, b in enumerate(connect)],
                y=connect,
                marker={'color': 'green',
                        'opacity': 0.8,
                        },
                showlegend=True,
                name='Connect')
    fig.add_bar(x=[a for a, b in enumerate(pair)],
                y=pair,
                marker={'color': 'blue',
                        'opacity': 0.8,
                        },
                showlegend=True,
                name='Pair')
    fig.write_html('{}.html'.format(args.file))


if __name__ == "__main__":
    main()
