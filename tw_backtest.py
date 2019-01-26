# -*- coding: utf-8 -*-
# @Time    : 2019/01/25 20:52
# @Author  : Ramble Dong
# @File    : get_AH_spread.py
import pandas as pd
import matplotlib.pyplot as plt


# get excel documents
xlsx_file = pd.ExcelFile("G:/data.xlsx")

# fetch the parses of excel and manage

tamsci = xlsx_file.parse(0)
tamsci = tamsci.T.drop(['Open', 'High',  'Low']).T
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

#
res1 = pd.merge(tamsci, twse)
res2 = pd.merge(fta, twa)
res = pd.merge(res1, res2)
res = res.dropna()
res['spread'] = res['close4']/res['close1']-res['close3']/res['close2']
res['Date'] = pd.to_datetime(res['Date'])
data = res.set_index(['Date'])
data = data.sort_index(ascending=True)

std_period = 8
data["std"] = data["spread"].rolling(std_period).std()
data["fair"] = data["spread"].rolling(std_period).mean()

print(data)


fair = 0
diverge_mul = 1
profit_mul = 1.5
skew = 0.0001

trades = []
qty = 20
lead_position = 0
max_position = 500
close_p2 = 0
close_p1 = 0
initial_balance = 1000000
hedge_ratio = 1/1.7
usdtwd = 30

for date, row in data.iterrows():
    if date < pd.to_datetime("2014-01-17"):
        continue
    diverge = diverge_mul * row["std"]
    profit_range = profit_mul * row["std"]
    # fair = row.fair

    p1 = fair - diverge - lead_position * skew
    p2 = fair + diverge - lead_position * skew
    close_p2 = p1 + profit_range - lead_position * skew
    close_p1 = p2 - profit_range - lead_position * skew

    if row.spread > p2 and lead_position > -max_position:

        trades.append({"date": date, "lead_qty": -qty, "hedge_qty": hedge_ratio * qty, "lead_price": row.close4,
                       "hedge_price": row.close3})
        lead_position -= qty

    elif row.spread < p1 and lead_position < max_position:
        trades.append({"date": date, "lead_qty": qty, "hedge_qty": -hedge_ratio * qty, "lead_price": row.close4,
                       "hedge_price": row.close3})
        lead_position += qty

    elif row.spread > close_p2 and lead_position > 0:
        trades.append({"date": date, "lead_qty": -qty, "hedge_qty": hedge_ratio * qty, "lead_price": row.close4,
                       "hedge_price": row.close3})
        lead_position -= qty

    elif row.spread < close_p1 and lead_position < 0:
        trades.append({"date": date, "lead_qty": qty, "hedge_qty": -hedge_ratio * qty, "lead_price": row.close4,
                       "hedge_price": row.close3})
        lead_position += qty

trades.append({"date": date, "lead_qty": -lead_position, "hedge_qty": hedge_ratio * lead_position,
               "lead_price": row.close4, "hedge_price": row.close3})

trade_record = pd.DataFrame(trades)
print(trade_record)

trade_record["lead_position"] = trade_record["lead_qty"].cumsum()
trade_record["hedge_position"] = trade_record["hedge_qty"].cumsum()

trade_record["hedge_account"] = - 200 * trade_record["hedge_qty"] * trade_record["hedge_price"] / usdtwd
trade_record["lead_account"] = - 100 * trade_record["lead_qty"] * trade_record["lead_price"]
trade_record["profit"] = trade_record["lead_account"].cumsum() + trade_record["hedge_account"].cumsum()
print(trade_record)

trade_record.to_excel("trade_record.xlsx")


data.plot(y=['spread'])
plt.title('plot_title')

trade_record.plot(y=['profit'])
plt.title('plot_title')
trade_record.plot(y=['lead_position'])
plt.title('plot_title')

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
fig.savefig('test2png.png', dpi=100)
plt.grid(axis="y", ls='--')
plt.show()
