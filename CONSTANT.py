import pandas as pd
import numpy as np
import os
import socket

host_name = socket.gethostname()
if host_name in ['jupiter']:
    data_root = '/13data/'
    simpnl_path = '/13data/liyz/project/intsim/bin/simpnl'
    simpnl_config_path = '/13data/liyz/project/intsim/config/config_simpnl.yaml'
elif host_name in ['jupitern']:
    data_root = '/mnt/13data/'
    simpnl_path = '/mnt/13data/liyz/intsim/bin/simpnl'
    simpnl_config_path = '/home/zhuq/simpnl/config/config_simpnl.yaml'   
elif host_name.startswith('research'):
    data_root = '/mnt/ResearchData/'
    simpnl_path = '/mnt/ResearchData/research/intsim/bin/simpnl'
    simpnl_config_path = '/mnt/ResearchData/research/intsim/config/config_simpnl.yaml'   
else:
    data_root = '/home/stock/'
    simpnl_path = '/home/stock/research/intsim/bin/simpnl'
    simpnl_config_path = '/home/stock/research/intsim/config/config_simpnl.yaml'

## TimeStamp
TIMESTAMP_24_STR = ['09:40:00', '09:50:00', '10:00:00', '10:10:00', '10:20:00', '10:30:00',
                    '10:40:00', '10:50:00', '11:00:00', '11:10:00', '11:20:00', '11:30:00',
                    '13:10:00', '13:20:00', '13:30:00', '13:40:00', '13:50:00', '14:00:00',
                    '14:10:00', '14:20:00', '14:30:00', '14:40:00', '14:50:00', '15:00:00']

TIMESTAMP_24_INT = [94000 ,95000 ,100000,101000,102000,103000,
                    104000,105000,110000,111000,112000,113000,
                    131000,132000,133000,134000,135000,140000,
                    141000,142000,143000,144000,145000,150000]

TIMESTAMP_48_STR     = ['09:35:00', '09:40:00', '09:45:00', '09:50:00', '09:55:00', '10:00:00', 
                       '10:05:00', '10:10:00', '10:15:00', '10:20:00', '10:25:00', '10:30:00',
                       '10:35:00', '10:40:00', '10:45:00', '10:50:00', '10:55:00', '11:00:00', 
                       '11:05:00', '11:10:00', '11:15:00', '11:20:00', '11:25:00', '11:30:00', 
                       '13:05:00', '13:10:00', '13:15:00', '13:20:00', '13:25:00', '13:30:00', 
                       '13:35:00', '13:40:00', '13:45:00', '13:50:00', '13:55:00', '14:00:00',
                       '14:05:00', '14:10:00', '14:15:00', '14:20:00', '14:25:00', '14:30:00', 
                       '14:35:00', '14:40:00', '14:45:00', '14:50:00', '14:55:00', '15:00:00']


## Tickers
tickers = (pd.read_csv(os.path.join(data_root, 'QuantData/DailyData/Info/csv/tickers'),index_col=0).iloc[:,0]).tolist()
TICKERS_INT = [int(s) for s in tickers]
TICKERS_STR = ['0'*(6-len(str(s)))+str(s) for s in tickers]

## Tradedays
CALENDAR = pd.read_csv(os.path.join(data_root, 'QuantData/DailyData/Info/csv/tradedays'),index_col=0).iloc[:,0].tolist()
