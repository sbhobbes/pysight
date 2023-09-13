import pandas as pd 
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import os 
import statsmodels.api as sm
import math
from .... import helper

def get_bricks_data():
    aus_df = helper.load_data('pysight\\fpp3\\assets\\data\\chapter_5\\aus_production.csv')
    aus_df['Quarter_date'] = aus_df['Quarter'].apply(helper.quarter_to_datetime)
    aus_df.set_index('Quarter', inplace = True)
    aus_df.drop(columns = ['Unnamed: 0'], inplace = True)
    bricks_df = aus_df.loc['1970 Q1' : '2004 Q4']
    bricks_df['mean_bricks'] = np.mean(bricks_df['Bricks'])

    return bricks_df

def get_forecast(df, value_col, ts_col, model, n_periods = 12, forecast_frequency = 'QS', seasonal_period = 4):
    MEAN = 'mean'
    NAIVE = 'naive'

    last_date = df[ts_col].iloc[-1]
    forecast_dates = pd.date_range(start = last_date, periods = n_periods, inclusive = 'right', freq = forecast_frequency)
    forecast_df = pd.DataFrame(forecast_dates, columns = [ts_col])
    forecast_df[value_col] = np.min(df[value_col])
    forecast_df['Quarter'] = forecast_df[ts_col].apply(helper.datetime_to_quarter)
    forecast_df.set_index('Quarter', inplace = True)

    if str.lower(model) == MEAN:
        pass
    elif str.lower(model) == NAIVE:
        forecast = df[value_col].tail(seasonal_period)
        forecast_addend = forecast.copy()
        repetitions = int(len(forecast_df) / seasonal_period)
        for rep in range(repetitions - 1):
            forecast = pd.concat([forecast, forecast_addend])
        forecast_df['seasonal_naive_bricks'] = forecast.values

    return forecast_df

def plot_mean_ts(df, n_periods, value_col, ts_col, forecast_frequency):
    mean_fc_df = get_forecast(df, value_col, ts_col, 'Mean', n_periods, forecast_frequency)
    plt.figure(figsize = (12, 7))
    sns.lineplot(data = df, x = df.index, y = 'Bricks', color = 'black')
    sns.lineplot(data = df, x = df.index, y = value_col, color = 'blue', linestyle = '--')
    sns.lineplot(data = mean_fc_df, x = mean_fc_df.index, y = value_col, color = 'blue')
    plt.title('Mean Forecast')
    ticks = plt.xticks()[0]
    plt.xticks(ticks[::10])
    plt.tight_layout()
    plt.show()

def plot_naive_ts(y_df, y_hat_df, y_col, y_hat_col):
    plt.figure(figsize = (12, 7))
    y_hat_df[y_hat_col] = y_df[y_col].iloc[-1]
    sns.lineplot(data = y_df, x = y_df.index, y = y_col, color = 'black')
    sns.lineplot(data = y_hat_df, x = y_hat_df.index, y = y_hat_col, color = 'blue')
    plt.title('Naive Forecast')
    ticks = plt.xticks()[0]
    plt.xticks(ticks[::10])
    plt.tight_layout()
    plt.show()

def some_simple_forecasting_methods():
    bricks_df = get_bricks_data()
    plot_mean_ts(bricks_df, 25, 'mean_bricks', 'Quarter_date', 'QS')

    # Seasonal Naive method
    # def seasonal_naive_forecast(series, seasonal_period):
    #     return series.tail(seasonal_period)

    # forecast = seasonal_naive_forecast(bricks_df['Bricks'], 4)
    # forecast = pd.concat([forecast, forecast, forecast, forecast, forecast, forecast])
    # forecast_df['seasonal_naive_bricks'] = forecast.values

    plt.figure(figsize = (12, 7))
    sns.lineplot(data = bricks_df, x = bricks_df.index, y = 'Bricks', color = 'black')
    sns.lineplot(data = forecast_df, x = forecast_df.index, y = 'seasonal_naive_bricks', color = 'blue')
    plt.title('Seasonal Nairve Forecast')
    plt.xticks(ticks[::10])
    plt.tight_layout()
    plt.show()

    # Random Walk / Drift method
    trend = np.arange(1, len(bricks_df) + 1)
    bricks_df['trend'] = trend
    forecast_df['trend'] = np.arange(len(bricks_df) + 1, len(bricks_df) + n_periods)

    first_y = bricks_df['Bricks'].head(1).values
    last_y = bricks_df['Bricks'].tail(1).values

    delta_y = last_y - first_y
    slope = delta_y / len(bricks_df)

    def get_drift_forecast(predict_series, index_series, slope, first_y):
        drift_values = [x * slope + first_y for x in predict_series]
        drift_df = pd.DataFrame(drift_values, columns = ['drift_bricks'])
        drift_df['trend'] = np.arange(np.min(index_series), np.max(index_series) + 1)
        return drift_df

    forecast_df = forecast_df.reset_index().merge(get_drift_forecast(forecast_df['trend'], forecast_df['trend'], slope, first_y), on = 'trend').set_index('Quarter')
    bricks_df['drift_bricks'] = bricks_df['trend'] * slope + first_y

    plt.figure(figsize = (12, 7))
    sns.lineplot(data = bricks_df, x = bricks_df.index, y = 'Bricks', color = 'black')
    sns.lineplot(data = bricks_df, x = bricks_df.index, y = 'drift_bricks', color = 'blue', linestyle = '--')
    sns.lineplot(data = forecast_df, x = forecast_df.index, y = 'drift_bricks', color = 'blue')
    plt.title('Drift Forecast')
    plt.xticks(ticks[::10])
    plt.tight_layout()
    plt.show()

    # Show 3 alongside actual data
    beer_df = aus_production_df.loc['1992 Q1' : '2006 Q4']
