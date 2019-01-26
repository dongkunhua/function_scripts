# -*- coding: utf-8 -*-
# @Time    : 2019/01/26 20:52
# @Author  : Ramble Dong
# @File    : get_store_excel_data_pandas_mannage.py
import pandas as pd
import matplotlib.pyplot as plt


# get excel documents
xlsx_file = pd.ExcelFile("G:/data.xlsx")

# fetch the parses of excel and manage
tamsci = xlsx_file.parse(0)
# delete some columns
tamsci = tamsci.drop(['Open', 'High',  'Low'], 1)
# rename the columns
tamsci.rename(columns={'Close': 'close1'}, inplace=True)

twse = xlsx_file.parse(1)
twse = twse.T.drop(['Open', 'High', 'Low']).T
twse.rename(columns={'Close': 'close2'}, inplace=True)

fta = xlsx_file.parse(2)
fta = fta.T.drop(['Open', 'High', 'Low']).T
fta.rename(columns={'Close': 'close3'}, inplace=True)

twa = xlsx_file.parse(3)
twa = twa.T.drop(['Open', 'High', 'Low']).T
twa.rename(columns={'Close': 'close4'}, inplace=True)

# combine the two dataframes by keys(same)
res1 = pd.merge(tamsci, twse)
res2 = pd.merge(fta, twa)
res = pd.merge(res1, res2)
res = res.dropna()

# combine two or more than two dataframes by keys(index)
# combine = tamsci.join(tamsci, twse, fta, twa, on='Date')
# print(combine)

res['spread'] = res['close4']/res['close1']-res['close3']/res['close2']
# convert to datetime
res['Date'] = pd.to_datetime(res['Date'])
# set index
data = res.set_index(['Date'])
# reverse
data = data.sort_index(ascending=True)
