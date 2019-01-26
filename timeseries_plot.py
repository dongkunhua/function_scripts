# -*- coding: utf-8 -*-
# @Time    : 2019/01/26 20:52
# @Author  : Ramble Dong
# @File    : timeseries_plot.py


import pandas as pd
import matplotlib.pyplot as plt
from collections import OrderedDict

xlsx_file = pd.ExcelFile("G:/data.xlsx")
tamsci = xlsx_file.parse(0)
tamsci['Date'] = pd.to_datetime(tamsci['Date'])
df = tamsci.set_index(['Date'])
df = df.sort_index(ascending=True)

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


def show_plot(frequency, step, columns, plot_title, tick_count=1000):
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

        plt.title(plot_title)
        plt.xlabel('Time')
        plt.ylabel('Spread')
        plt.grid(axis="y", ls='--')
        plt.show()


plot_title = 'tamsci'
show_plot('month', 1, ['Open', 'Close'], plot_title, tick_count=1000)
