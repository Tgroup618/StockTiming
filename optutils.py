import pandas as pd 
import numpy as np 
import os
from CONSTANT import *

dividend_record_path = os.path.join(data_root, 'QuantData/DailyData/DividendRecord/csv/DividendRecord')

def get_prev_date(date):
    result = CALENDAR
    result = list(filter(lambda x:x<date, result))
    result.sort()
    return result[-1]

def get_next_date(date):
    result = CALENDAR 
    result = list(filter(lambda x:x>date, result))
    result.sort()
    return result[0]


def get_calendar(begin_date, end_date):
    try:
        result = CALENDAR
        result = list(filter(lambda x: x>= begin_date, result))
        result = list(filter(lambda x: x<= end_date,   result))
        result.sort()
        return result
    except:
        return []


def time_int2str(int_time: int):
    str_time = str(int(int_time))
    return '{} {}:{}:{}'.format(str_time[:8], str_time[8:10], str_time[10:12], str_time[12:14])

def timestamp_daily2min(tradedays: list, timestamps: list):
    nDate = len(tradedays)
    nTimestamp = len(timestamps)
    tradedays = [int(str(s).replace('-', '')) for s in tradedays]
    result = np.zeros(nDate*nTimestamp, dtype='int')
    timestamp_int = np.array([int(s.replace(':', ''))
                                  for s in timestamps])

    ptr = 0
    for date in tradedays:
        result[ptr:ptr+nTimestamp] = timestamp_int + date*1e6
        ptr += nTimestamp

    result = list(result)
    result = [time_int2str(s) for s in result]
    return result


def get_share_per_roundlot(code):
    return 200 if code.startswith('688') else 100 


def legal_target_share(holding, avai_sell, target_share, share_per_roundlot):
    delta = target_share - holding
    if delta>=0:
        round_delta = round(delta / share_per_roundlot) * share_per_roundlot 
        final_target = holding + round_delta 
    else:
        neg_round_delta = - round(delta / share_per_roundlot) * share_per_roundlot
        sell_share = min(avai_sell, neg_round_delta)
        if holding - sell_share < share_per_roundlot:
            sell_share = avai_sell
        final_target = holding - sell_share 
    return final_target


def get_dividend_record(begin_date=20000101, end_date=29991231):
    df = pd.read_csv(dividend_record_path, index_col=0)
    df['Code'] = ['0'*(6-len(str(s)))+str(s) for s in df['Code']]
    df['Date'] = [int(s) for s in df['Date']]
    df = df.set_index(['Date','Code'],drop=True).loc[begin_date:end_date]
    share_ratio = 1 + df['bonus_share_ratio'] + df['conversed_ratio'] + df['rightsissue_ratio'] - (1-df['consolidate_split_ratio'])
    cash_ratio = df['cash_dividend_ratio'] - df['rightsissue_ratio']*df['rightsissue_price']
    return share_ratio, cash_ratio

def test_dividend_record(begin_date=20200101, end_date=20201231):
    share_ratio, cash_ratio = get_dividend_record(begin_date, end_date)

    close = pd.read_csv('/13data/QuantData/DailyData/PVData/PV/csv/close',index_col=0).loc[begin_date:end_date]
    preclose = pd.read_csv('/13data/QuantData/DailyData/PVData/PV/csv/preclose',index_col=0).loc[begin_date:end_date]

    for date in close.index[1:]:
        if date in share_ratio.index:
            share_today = share_ratio.loc[date]
            cash_today = cash_ratio.loc[date]

            close_yesterday = close.loc[get_prev_date(date),share_today.index]
            preclose_today = preclose.loc[date,share_today.index]    

            left = 1*close_yesterday
            right = share_today*preclose_today + cash_today
            diff = left-right
            delta = diff[abs(diff)>=1e-2].dropna()
            if delta.shape[0]>0:
                print(date, delta)


if __name__ == "__main__":
    test_dividend_record(20200101,20201231)
