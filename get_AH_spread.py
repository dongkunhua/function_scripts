# -*- coding: utf-8 -*-
# @Time    : 2019/01/24 20:52
# @Author  : Ramble Dong
# @File    : get_AH_spread.py

from pymongo import MongoClient
import pandas as pd
import matplotlib.pyplot as plt
from collections import OrderedDict


# set the global variable
# connect the database of cloud servers
client = MongoClient(
    host='113.108.181.146',
    port=27701, username='aduser1',
    password='ok1b8W@8YKg3P8%i'
)
code = ['00390.HK_601390.SH', '00753.HK_601111.SH', '01211.HK_002594.SZ', '02318.HK_601318.SH',
        '02333.HK_601633.SH', '02338.HK_000338.SZ', '02628.HK_601628.SH', '02883.HK_601808.SH',
        '03968.HK_600036.SH']
for collection in code:
    # get  database
    strategy_status = client["strategy_status"]

    # get a collection and show the first documents and its numbers
    coll = strategy_status[collection]

    # convert the collection to dataframe
    data = pd.DataFrame(list(coll.find()))

    # delete the fields unwanted
    df = data.T.drop(['_id', 'delta_hedge', 'hedge_position', 'lead_position',   'timestamp']).T
    df.record_time = pd.to_datetime(df.record_time)
    # set the "time" as index
    df = df.set_index(['record_time'])

    pd.set_option('display.expand_frame_repr', False)
    rng_date = df.index
    df = df.reset_index()

    # Solve the time series discontinuity problem
    def tick_category(frequency, step):
        """
        Gets the time axis of the scale based on frequency and frequency number
        frequency  value for: 'year','month','day','hour','minute','second'
        :param frequency:
        :param step:
        :return:
        """
        if frequency == 'year':
            df['frequency'] = rng_date.strftime('%Y')
        elif frequency == 'month':
            df['frequency'] = rng_date.strftime('%Y-%m')
        elif frequency == 'day':
            df['frequency'] = rng_date.strftime('%Y-%m-%d')
        elif frequency == 'hour':
            df['frequency'] = rng_date.strftime('%Y-%m-%d %H')
        elif frequency == 'minute':
            df['frequency'] = rng_date.strftime('%Y-%m-%d %H:%M')
        elif frequency == 'second':
            df['frequency'] = rng_date.strftime('%Y-%m-%d %H:%M:%S')
        else:
            df['frequency'] = rng_date.strftime('%Y')

        num_date = OrderedDict()
        for item in df.groupby('frequency'):
            num_date[item[1].index[-1]] = item[0]

        nums = list(num_date.keys())[::step]
        dates = list(num_date.values())[::step]
        return num_date, nums, dates


    def show_plot(frequency, step, columns, collect, tick_count=1000):
        num_date, nums, dates = tick_category(frequency, step)
        end_pos = nums[tick_count] if tick_count < len(nums) else nums[-1]
        data = df.loc[:, columns][:end_pos]
        axes = data.plot()
        axes.set_xticks(nums[:end_pos])
        axes.set_xticklabels(dates[:end_pos], rotation=45)

        ax = plt.gca()
        ax.spines['top'].set_visible(False)  # remove the rop spine
        # ax.spines['bottom'].set_visible(False) #remove the bottom spine
        ax.spines['left'].set_visible(False)  # remove the left spine
        ax.spines['right'].set_visible(False)  # remove the right spine
        # ax.spines['left'].set_linewidth(0.5)
        ax.spines['bottom'].set_linewidth(0.2)
        # ax.spines['right'].set_linewidth(0.5)
        # ax.spines['top'].set_linewidth(0.5)

        fig = plt.gcf()
        fig.set_size_inches(18.5, 3.5)

        plt.title(collect)
        plt.xlabel('Time')
        plt.ylabel('Spread')
        plt.grid(axis="y", ls='--')
        plt.show()

    show_plot('month', 1, ['spread_bid', 'spread_ask'], collection, tick_count=1000)
