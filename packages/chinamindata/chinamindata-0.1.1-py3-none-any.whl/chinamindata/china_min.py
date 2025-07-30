

import requests
import pandas as pd
import time

from fastapi import params
from change_time import get_monthly_first_days
from chinamindata.c_min import get_token
from datetime import datetime, timedelta

def pro_bar1(code, start_date, end_date,limit='8000',offset='0',freq='60min'):
    """
    Fetch stock data from a given URL with specified parameters.

    Parameters:

    ts_code (str): The stock code to fetch data for.
    start_date (str): The start date for fetching data (in 'YYYY-MM-DD HH:MM:SS' format).
    end_date (str): The end date for fetching data (in 'YYYY-MM-DD HH:MM:SS' format).
    freq (str): The frequency of the data (e.g., '1min', '5min'，'15min', '30min'， '60min').
    token (str): The access token for the data source. Default is provided.
    offset (str, 可选): 数据偏移量，用于分页获取数据，默认为'0'。当需要获取更多数据时，可以增大此值。
    freq (str, 可选): 数据频率，指定返回数据的时间间隔，例如'1min'（1分钟）、'5min'（5分钟）、'15min'（15分钟）、
                      '30min'（30分钟）、'60min'（60分钟，即1小时）等。默认为'60min'。

    Returns:
    pd.DataFrame: A DataFrame containing the fetched stock data.
    """

    # url = "http://localhost:9002/c_min"
    url='http://39.105.209.102:8002/c_min'
    params = {

        'ts_code': code,
        'start_date': start_date,
        'end_date': end_date,
        'freq': freq,
        'limit':limit,
        'offset':offset,
        'token': get_token()
    }


    # print(type(process_dates(start_date, end_date,freq)))
    if type(process_dates(start_date, end_date,freq)) == tuple:

        processed_start, processed_end = process_dates(start_date, end_date,freq)
        return gg_min(code, processed_start, processed_end,freq)

    else:
        result=process_dates(start_date, end_date,freq)

        combined_df = pd.DataFrame()
        for idx in range(len(result)-1):
            # print(result)
            # 获取当前区间参数
            start_date1 = result[idx]
            end_date1 = result[idx + 1] if idx < len(result) - 1 else result[idx]
            star_date1 = var_dates(start_date1)
            end_date2=var_dates(end_date1)


            df=gg_min(code, star_date1, end_date2, freq)
            # print(df)

            if df.empty:
                pass
                # print(code+start_date+ end_date+'数据为空')
            else:

                combined_df = pd.concat([combined_df, df], ignore_index=True)

            if combined_df.empty:
                print(code + '部分数据为空，请注意开始时间和结束时间')
            else:

                combined_df = combined_df.sort_values('trade_time', ascending=False)
                # print(combined_df)

                # 去重（根据需求决定是否保留最新记录）
                combined_df = combined_df.drop_duplicates(subset=['trade_time'], keep='first').reset_index(drop=True)
        combined_df['trade_time'] = pd.to_datetime(combined_df['trade_time'])
        # print(start_date, end_date)
        filtered_df = combined_df[combined_df['trade_time'].between(start_date, end_date)].reset_index(drop=True)
        # print(filtered_df)
        return filtered_df









def gg_min(code,processed_start,processed_end,freq):
    url = 'http://39.105.209.102:8005/china/stock/min/' + code + '/' + processed_start + '/' + processed_end + '/' + freq + '/E/' + get_token()
    # print(url)
    response = requests.get(url)

    if response.status_code == 200:
        try:

            data = response.json()
            # print(data)
            if data == 'token无效或已超期,请重新购买':
                raise ValueError(data)
            else:

                df = pd.DataFrame(data)
                if df.empty:
                    return df
                else:
                    # print(df)
                    df["trade_time"] = pd.to_datetime(df["trade_time"], unit='s').astype('object')

                    df_sorted = df.sort_values('trade_time', ascending=False).reset_index(drop=True)
                    # print(df_sorted)
                    return df_sorted
        except ValueError as e:
            print("Error parsing JSON response:", e)
            return None
    else:
        print(f"Failed to fetch data. Status code: {response.status_code}")
        print(response.text)
        return None

def process_dates(start_date, end_date,freq):
    # 处理start_date
    if len(start_date.split()) == 1:  # 只有日期部分
        start_date += " 00:00:01"

    # 处理end_date
    if len(end_date.split()) == 1:  # 只有日期部分
        end_date += " 23:30:01"

    date_format = "%Y-%m-%d %H:%M:%S"
    start_dt = datetime.strptime(start_date, date_format)
    end_dt = datetime.strptime(end_date, date_format)

    # 计算时间跨度
    delta = end_dt - start_dt
    if delta.days > 33:  # 超过1个月
        ll=get_monthly_first_days(start_dt, end_dt,freq)
        # 调用其他处理函数
        return ll
    else:

        return start_date, end_date

def var_dates(s_date):
    # 处理start_date
    # print(s_date.split())
    if len(s_date.split()) == 1:  # 只有日期部分
        s_date += " 00:00:01"
    return s_date













