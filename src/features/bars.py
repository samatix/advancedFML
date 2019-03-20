import pandas as pd
import numpy as np


def tick_bar(df, m):
    """
    Tick bar function
    :param df: Dataframe entry that contains the prices time series
    Example:
                                        price     bid     ask   vol   dollar_vol
            date
            2019-03-18 15:49:35  114.4643  114.46  114.47   500   57232.1500
            2019-03-18 15:49:35  114.4643  114.46  114.47  2520  288450.0360
    :param m: The number of steps when to take the tick information
    :return: a dataframe of tick information
    Example:
                                        price     bid     ask  vol  dollar_vol
            date
            2019-03-18 15:49:35  114.4643  114.46  114.47  500    57232.15
            2019-03-18 15:55:00  114.3700  114.38  114.39  200    22874.00

    """
    return df.iloc[::m]


def volume_bar(df, m):
    """
    Volume bars
    TODO: Can be optimized
    :param df: Dataframe entry that contains the prices time series
    Example:
                                        price     bid     ask   vol   dollar_vol
            date
            2019-03-18 15:49:35  114.4643  114.46  114.47   500   57232.1500
            2019-03-18 15:49:35  114.4643  114.46  114.47  2520  288450.0360
    :param m: Volume threshold
    :return:
    Example:
                                    price     bid     ask   vol   dollar_vol  cum_vol
            date
            2019-03-18 15:49:35  114.4643  114.46  114.47  2520  288450.0360     3020
            2019-03-18 15:54:00  114.4200  114.41  114.42   147   16819.7400     1071
            2019-03-18 15:54:00  114.4300  114.42  114.43  2100  240303.0000     2100
    """
    aux = df.reset_index()
    idx = []
    vol_acum = []
    c_v = 0
    for i, v in aux.vol.items():
        c_v = c_v + v
        if c_v >= m:
            idx.append(i)
            vol_acum.append(c_v)
            c_v = 0
    volume_bar = aux.loc[idx]
    volume_bar.loc[idx, 'cum_vol'] = vol_acum
    volume_bar = volume_bar.set_index('date')
    return volume_bar


def dollar_bar(df, m):
    """
    Dollar bars
    TODO: Can be optimized
    :param df: Dataframe entry that contains the prices time series
    Example:
                                        price     bid     ask   vol   dollar_vol
            date
            2019-03-18 15:49:35  114.4643  114.46  114.47   500   57232.1500
            2019-03-18 15:49:35  114.4643  114.46  114.47  2520  288450.0360
    :param m: Dollar amount threshold
    :return:
    Example:
                                    price     bid     ask   vol   dollar_vol  \
            date
            2019-03-18 15:49:35  114.4643  114.46  114.47  2520  288450.0360
            2019-03-18 15:53:49  114.4100  114.41  114.41   200   22882.0000
            2019-03-18 15:54:00  114.4300  114.42  114.43  2100  240303.0000
                                    cum_dollar_vol
            date
            2019-03-18 15:49:35     345682.1860
            2019-03-18 15:53:49     105727.1720
            2019-03-18 15:54:00     257122.7400
    """
    aux = df.reset_index()
    idx = []
    d_acum = []
    c_dv = 0
    for i, dv in aux.dollar_vol.items():
        c_dv = c_dv + dv
        if c_dv >= m:
            idx.append(i)
            d_acum.append(c_dv)
            c_dv = 0
    dollar_bar = aux.loc[idx]
    dollar_bar.loc[idx, 'cum_dollar_vol'] = d_acum
    dollar_bar = dollar_bar.set_index('date')
    return dollar_bar


def volume_bar_cum(df, m):
    aux = df.reset_index()
    cum_v = aux.vol.cumsum()
    th = m
    idx = []
    for i, c_v in cum_v.items():
        if c_v >= th:
            th = th + m
            idx.append(i)
    return aux.loc[idx].set_index('date')


def dollar_bar_cum(df, m):
    aux = df.reset_index()
    cum_dv = aux.dollar_vol.cumsum()
    th = m
    idx = []
    for i, c_dv in cum_dv.items():
        if c_dv >= th:
            th = th + m
            idx.append(i)
    return aux.loc[idx].set_index('date')
