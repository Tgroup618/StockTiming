import pandas as pd 
import numpy as np 
from optutils import *
from CONSTANT import * 
import os
import h5py
def read_daily_data(filepath):
    df = pd.read_csv(filepath, index_col=0, parse_dates=[0])
    df.index = [s.strftime("%Y%m%d") for s in df.index]
    return df
def read_tick_data(filepath, filetype = 'csv'):
    if filetype=='csv':
        df = pd.read_csv(filepath, index_col=0, parse_dates=[0])
        df.index = [s.strftime("%Y%m%d %H:%M:%S") for s in df.index]
    elif filetype == 'pkl':
        df = pd.read_pickle(filepath)
    return df
def get_files_with_string(directory, string):
    files = os.listdir(directory)
    matching_files = [file for file in files if string in file]
    return matching_files
def check_date_daily_file(date:str, filepath:str):
    if not os.path.exists(filepath):
        print(f'{filepath} missing')
        return 0
    df = read_daily_data(filepath)
    if date in df.index:
        print(f'{filepath} is OK!')
    else:
        print(f'{filepath} missing date:{date}')
def check_date_tick_file(date:str, filepath:str):
    if not os.path.exists(filepath):
        print(f'{filepath} missing')
        return 0
    df = read_tick_data(filepath)
    date_ticks = 0
    for x in df.index:
        if x[0:8] == date:
            date_ticks += 1
    if date_ticks == 48:
        print(f'{filepath} is OK!')
    else:
        print(f'{filepath} missing date:{date}, date_ticks:{date_ticks}')
def get_ic_df_columns_mean(df_x, df_y):
    cols = df_x.columns
    res = np.array([np.corrcoef(df_x[col][np.isfinite(df_x[col]) & np.isfinite(df_y[col])], df_y[col][np.isfinite(df_x[col]) & np.isfinite(df_y[col])])[0,1] for col in cols])
    return np.mean(res[np.isfinite(res)])
def get_ic_df(df_x, df_y):
    x = np.array(df_x).flatten()
    y = np.array(df_y).flatten()
    return np.corrcoef(x[np.isfinite(x) & np.isfinite(y)], y[np.isfinite(x) & np.isfinite(y)])[0,1]
def get_quantile(df, pct):
    return np.nanpercentile(np.array(df), pct)

def load_feature(dates, feature_name = 'BasicFeatures_TWAP'):
    if len(dates) == 0:
        return pd.DataFrame()
    feature_tb = []
    for date_int in dates:
        date = str(date_int)
        feature_tb_file = f'{data_root}Features/5min/{date}/{feature_name}.h5'
        f = h5py.File(feature_tb_file,'r')
        data = np.array(f['data'])
        index = np.array(f['timestamp'])/1000
        columns = np.array(f['stock'])
        columns = [str(s).zfill(6) for s in columns]
        feature = pd.DataFrame(data,index=[date+ ' ' + str(int(s)).zfill(6)[0:2]+':'+str(int(s)).zfill(6)[2:4]+':'+str(int(s)).zfill(6)[4:6] for s in index],columns=columns)
        # Close_tb = (Close_tb.sum(axis=1)/np.isfinite(Close_tb).sum(axis =1)).plot()
        feature_tb.append(feature)
    feature_tb = pd.concat(feature_tb, axis = 0)
    return feature_tb

import matplotlib.pyplot as plt
def plot_tick(df, title = 'value'):
    df = pd.DataFrame(df)
    plt.figure(figsize = (12, 5))
    new_tick = range(len(df))
    for col in df.columns:
        plt.plot(new_tick, df.loc[:, col])
    plt.xticks(new_tick, [x  if x[-8:] in ['09:30:00', '10:30:00', '11:30:00', '14:00:00'] else '' for x in df.index], rotation = 90)
    plt.legend(df.columns)
    plt.xlabel('Time')
    plt.ylabel('Value')
    plt.title(f't vs {title}')
    plt.show()
def plot_daily(df, title = 'value'):
    df = pd.DataFrame(df)
    days = CALENDAR
    first_in_month = list(pd.DataFrame(days, index = [str(x) for x in days]).groupby(lambda x:x[0:6]).first().iloc[:,0])
    plt.figure(figsize = (20, 6))
    new_tick = range(len(df))
    for col in df.columns:
        plt.plot(new_tick, df.loc[:, col])
    plt.xticks(new_tick, [x[0:8] if int(x[0:8]) in first_in_month else '' for x in df.index], rotation = 90)
    plt.legend(df.columns, loc = 'upper left')
    plt.xlabel('Time')
    plt.ylabel('Value')
    plt.title(f't vs {title}')
    plt.show()