import pandas as pd
import yfinance as yf
import numpy as np
import matplotlib.pyplot as plt

datos = yf.download("BTC-USD")

def data(date, s, l):
    df = date.copy()
    df["SMAs"] = df.Close.rolling(s).mean()
    df["SMAl"] = df.Close.rolling(l).mean()    
    df = df.filter(["Date", "Close", "Open", "SMAs", "SMAl"], axis = 1)
    return df

df = data(datos, 50, 200)
long_positions = np.where(df['SMAs'] > df['SMAl'], 1, 0)
df['Position'] = long_positions

buy_signals = (df['Position'] == 1) & (df['Position'].shift(1) == 0)
df.loc[buy_signals].round(3)

buy_signals_prev = (df['Position'].shift(-1) == 1) & (df['Position'] == 0)
df.loc[buy_signals | buy_signals_prev].round(3)

# The returns of the Buy and Hold strategy:
df['Hold'] = np.log(df['Close'] / df['Close'].shift(1))
df["Lineales"] = df['Close'] / df['Close'].shift(1) - 1

# The returns of the Moving Average strategy:
df['Strategy'] = df['Position'].shift(1) * df['Hold']
# We need to get rid of the NaN generated in the first row:
df.dropna(inplace=True)

returns = np.exp(df[['Hold', 'Strategy']].sum()) - 1
print(f"Buy and hold return: {round(returns['Hold']*100,2)}%")
print(f"Strategy return: {round(returns['Strategy']*100,2)}%")
