import pandas as pd
import numpy as np
import sys
import plotly.graph_objs as go
import argparse


def parseargs():
    '''
    Argument Parser - Parses arguments passed to the file
    Expected arguments: --file <file>
    
    Returns:
        args
    '''
    parser = argparse.ArgumentParser()
    parser.add_argument('--file')

    args = parser.parse_args(None if sys.argv[1:] else ['-h'])

    return args


def create_df(args):
    '''
    Create dataframe from the file passed via "--file" argument
    
    Returns:
        df
    '''
    df = pd.read_csv(args.file, header=None, names=[
                     'Time', 'Iteration', 'Test Case', 'Result',
                     'Scan', 'Connect', 'Pair', ''])
    return df


def clean_df(df):
    '''
    Clean dataframe by removing rows with "OTHER ERROS" or without iteration data
    
    Returns:
        df
    '''
    df = df[df['Result'] != " <OTHER ERROR>"]
    df = df[df['Iteration'].str.startswith(' ', na=False)]
    df.replace(' ', 0, inplace=True)
    return df


def split_list(my_list):
    '''
    Split the string in the list items to return the numerical part of the string
    
    Returns:
        new_list
    '''
    new_list = []
    for item in my_list:
        new_item = str(item).split()
        if len(new_item) > 1:
            new_list.append(new_item[-2])
        else:
            new_list.append(new_item[0])

    return new_list


def get_stats(my_list):
    '''
    Generate stats for the list of integers
    
    Returns: 
    max_val, min_val, mean_val 
    '''
    np_array = np.array(my_list).astype(np.float)
    # print(dir(np_array))
    max_val = np_array.max()
    min_val = np_array.min()
    mean_val = np_array.mean()
    return max_val, min_val, mean_val


def put_stats_to_list(max_val, min_val, mean_val):
    '''
    Generate a list of stats provided to add to the graph
    
    Returns:
        mylist
    '''
    mylist = [
        ('Max', round(max_val, 2)),
        ('Min', round(min_val, 2)),
        ('Mean', round(mean_val, 2))
    ]
    return mylist

def draw_figure(fig, mylist, color='red', myname='Generic', mydict={}):
    '''
    Add plot to the figure and return the figure
    
    Returns:
        fig
    '''
    fig.add_scatter(x=[a for a, b in enumerate(mylist)],
                y=mylist,
                # mode='markers',
                marker={
                    'size':4,
                    # 'line':{'width':1},
                    'opacity': 0.8,
                    'color':color},
                text=str(mydict),
                showlegend=True,
                name=myname)
    return fig


def main():
    args = parseargs()
    df = create_df(args)
    df = clean_df(df)
    scan_list = df['Scan']
    connect_list = df['Connect']
    pair_list = df['Pair']
    scan = split_list(scan_list)
    max_scan, min_scan, mean_scan = get_stats(scan)
    connect = split_list(connect_list)
    max_connect, min_connect, mean_connect = get_stats(connect)
    pair = split_list(pair_list)
    max_pair, min_pair, mean_pair = get_stats(pair)
    scan_stats = put_stats_to_list(max_scan, min_scan, mean_scan)
    connect_stats = put_stats_to_list(max_connect, min_connect, mean_connect)
    pair_stats = put_stats_to_list(max_pair, min_pair, mean_pair)
    print('Scan: {}, Number of values: {}'.format(
        scan_stats, len(scan)))
    print('Connect: {}, Number of values: {}'.format(
        connect_stats, len(connect)))
    print('Pair: {}, Number of values: {}'.format(
        pair_stats, len(pair)))
    fig = go.FigureWidget()
    draw_figure(fig, scan, 'orange', 'Scan', scan_stats)
    draw_figure(fig, connect, 'green', 'Connect', connect_stats)
    draw_figure(fig, pair, 'blue', 'Pair', pair_stats)
    
    fig.write_html('{}.html'.format(args.file))


if __name__ == "__main__":
    main()
