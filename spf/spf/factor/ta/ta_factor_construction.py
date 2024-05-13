from pandas import DataFrame
import pandas as pd
import numpy as np
import talib.abstract as tab


# feel free to add or subtract more indicators for any other strategy you want to use
def populateindicators(dataframe) -> DataFrame:
    # make sure to remove these later
    # exponential moving averages
    dataframe['sema_high'] = tab.EMA(dataframe, timeperiod=12, price='high')
    dataframe['fema_high'] = tab.EMA(dataframe, timeperiod=5, price='high')
    dataframe['ema_close'] = tab.EMA(dataframe, timeperiod=5, price='close')
    dataframe['ema_low'] = tab.EMA(dataframe, timeperiod=5, price='low')
    dataframe['dema'] = tab.DEMA(dataframe['close'], timeperiod=30)

    # mathematics

    macd = tab.MACD(dataframe, fastperiod=12, slowperiod=26, signalperiod=9)
    # dataframe['macd'] = macd['macd']
    dataframe['macdsignal'] = macd['macdsignal']
    dataframe['macdhist'] = macd['macdhist']

    # stochastics
    #stoch_fast = tab.STOCHF(dataframe, 10.0, 3.0, 0.0, 3.0, 0.0)
    #stoch = tab.STOCH(dataframe, fastk_period=5, slowk_period=3, slowk_matype=0, slowd_period=3, slowd_matype=0)
    #stoch_rsi = tab.STOCHRSI(dataframe, timeperiod=14, fastk_period=5, fastd_period=3, fastd_matype=0)

    # dataframe['slowd'] = stoch['slowd']
    # dataframe['slowk'] = stoch['slowk']

    #dataframe['fastdf'] = stoch_fast['fastd']
    #dataframe['fastkf'] = stoch_fast['fastk']

    #dataframe['fastdrsi'] = stoch_rsi['fastd']
    #dataframe['fastkrsi'] = stoch_rsi['fastk']

    # momentum indicators
    # dataframe['willr'] = tab.WILLR(dataframe['high'].values, dataframe['low'].values, dataframe['close'].values)
    dataframe['ultosc'] = tab.ULTOSC(dataframe)

    dataframe['mfi'] = tab.MFI(dataframe['high'], dataframe['low'], dataframe['close'],
                              np.asarray(dataframe['volume'], dtype='float'), timeperiod=14)
    # dataframe['smfi'] = ta.MFI(dataframe['high'], dataframe['low'], dataframe['close'], np.asarray(dataframe['volume'], dtype='float'), timeperiod=20)
    # dataframe['fmfi'] = ta.MFI(dataframe['high'], dataframe['low'], dataframe['close'], np.asarray(dataframe['volume'], dtype='float'), timeperiod=8)

    dataframe['adx'] = tab.ADX(dataframe)
    # dataframe['fadx'] = tab.ADX(dataframe, timeperiod=8)
    # dataframe['sadx'] = tab.ADX(dataframe, timeperiod=20)

    dataframe['adxr'] = tab.ADXR(dataframe)

    # dataframe['adxr'] = tab.ADXR(dataframe)

    dataframe['cci'] = tab.CCI(dataframe)
    dataframe['rsi2'] = tab.RSI(dataframe, timeperiod=14)
    dataframe['rocr'] = tab.ROCR(dataframe)

    dataframe['plus_di'] = tab.PLUS_DI(dataframe)
    dataframe['minus_di'] = tab.MINUS_DI(dataframe)
    dataframe['mom'] = tab.MOM(dataframe)

    # statistics
    # dataframe['sbeta']=tab.BETA(dataframe, timeperiod=9)
    dataframe['beta'] = tab.BETA(dataframe, timeperiod=5)
    # dataframe['fbeta']=tab.BETA(dataframe, timeperiod=3)

    # dataframe['scorrel']=tab.CORREL(dataframe, timeperiod=30)
    dataframe['correl'] = tab.CORREL(dataframe, timeperiod=17)
    # dataframe['fcorrel']=tab.CORREL(dataframe, timeperiod=10)

    # dataframe['svar']=tab.VAR(dataframe, timeperiod=8)
    dataframe['var'] = tab.VAR(dataframe, timeperiod=5)
    # dataframe['fvar']=tab.VAR(dataframe, timeperiod=3)
    # dataframe['linearreg']=tab.LINEARREG(dataframe, timeperiod=10)
    dataframe['linearreg_angle'] = tab.LINEARREG_ANGLE(dataframe, timeperiod=10)
    dataframe['linear_slope'] = tab.LINEARREG_SLOPE(dataframe, timeperiod=10)
    # dataframe['tsf']=tab.TSF(dataframe, timeperiod=14)
    # create time indicators
    # dataframe['months']=dataframe.index.get_level_values(level='timestamp').month
    # dataframe['dayofweek']=dataframe.index.get_level_values(level='timestamp').dayofweek
    # dataframe['hourofday']=dataframe.index.get_level_values(level='timestamp').hour

    # required for graphing
    bollinger = tab.BBANDS(dataframe.close, timeperiod=5, nbdevup=1.7, nbdevdn=1.7)
    dataframe['bb_lowerband'] = bollinger[2]
    dataframe['bb_upperband'] = bollinger[0]
    dataframe['bb_middleband'] = bollinger[1]

    # create volume based indicators
    dataframe['adosc'] = tab.ADOSC(dataframe['high'], dataframe['low'], dataframe['close'],
                                  np.asarray(dataframe['volume'], dtype='float'))
    # dataframe['ad']=ta.AD(dataframe['high'], dataframe['low'], dataframe['close'], np.asarray(dataframe['volume'], dtype='float'))
    # dataframe['obv']=ta.OBV(dataframe['close'], np.asarray(dataframe['volume'], dtype='float'))
    # Create volatility indicator
    dataframe['natr'] = tab.NATR(dataframe)

    # create row of labels/classification
    # if dataframe
    # dataframe['maxindex'] = tab.MAXINDEX(dataframe, timeperiod=30)

    return dataframe


# Compute RSI
def relative_strength_index(df, n):
    """Calculate Relative Strength Index(RSI) for given data.
    https://github.com/Crypto-toolbox/pandas-technical-indicators/blob/master/technical_indicators.py

    :param df: pandas.DataFrame
    :param n:
    :return: pandas.DataFrame
    """
    i = 0
    UpI = [0]
    DoI = [0]
    while i + 1 <= df.index[-1]:
        UpMove = df.loc[i + 1, 'high'] - df.loc[i, 'high']
        DoMove = df.loc[i, 'low'] - df.loc[i + 1, 'low']
        if UpMove > DoMove and UpMove > 0:
            UpD = UpMove
        else:
            UpD = 0
        UpI.append(UpD)
        if DoMove > UpMove and DoMove > 0:
            DoD = DoMove
        else:
            DoD = 0
        DoI.append(DoD)
        i = i + 1
    UpI = pd.Series(UpI)
    DoI = pd.Series(DoI)
    PosDI = pd.Series(UpI.ewm(span=n, min_periods=n).mean())
    NegDI = pd.Series(DoI.ewm(span=n, min_periods=n).mean())
    RSI = pd.Series(round(PosDI * 100. / (PosDI + NegDI)), name='RSI_' + str(n))
    # df = df.join(RSI)
    return RSI


def get_rsi(data, window=14):
    df = data.copy(deep=True).reset_index()
    rsi = relative_strength_index(df, window)
    rsi_df = pd.Series(data=rsi.values, index=data.index)
    return rsi_df

def bbands(close_prices, window, no_of_stdev):
    # rolling_mean = close_prices.rolling(window=window).mean()
    # rolling_std = close_prices.rolling(window=window).std()
    rolling_mean = close_prices.ewm(span=window).mean()
    rolling_std = close_prices.ewm(span=window).std()

    upper_band = rolling_mean + (rolling_std * no_of_stdev)
    lower_band = rolling_mean - (rolling_std * no_of_stdev)

    return rolling_mean, upper_band, lower_band