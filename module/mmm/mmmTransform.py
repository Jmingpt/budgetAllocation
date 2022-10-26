import pandas as pd
import numpy as np


def row_to_pivot(df):
    date_range = '{} - {}'.format(df['Date'].min().strftime('%Y/%m/%d'), df['Date'].max().strftime('%Y/%m/%d'))
    pivot_tb = pd.pivot_table(df, values='Cost', index=['Date'], columns=['Channel'], aggfunc=np.sum)
    pivot_df = pivot_tb.reset_index().sort_values('Date', ascending=False).reset_index(drop=True)
    pivot_df = pivot_df.fillna(0)
    revenue_df = df.groupby('Date') \
                   .agg({'Revenue': np.sum}) \
                   .reset_index() \
                   .sort_values('Date', ascending=False) \
                   .reset_index(drop=True)
    mmm = pd.merge(pivot_df, revenue_df, on='Date', how='left')
    mmm_df = mmm.set_index('Date')

    return date_range, mmm_df
