import pandas as pd 
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import os 
import statsmodels.api as sm
from ... import helper

def get_bricks_data():
    aus_df = helper.load_data('pysight\\assets\\data\\chapter_5\\aus_production.csv')
    aus_df['Quarter_date'] = aus_df['Quarter'].apply(helper.quarter_to_datetime)
    aus_df.set_index('Quarter', inplace = True)
    aus_df.drop(columns = ['Unnamed: 0'], inplace = True)
    bricks_df = aus_df.loc['1970 Q1' : '2004 Q4']
    bricks_df['mean_bricks'] = np.mean(bricks_df['Bricks'])

    return bricks_df



def some_simple_forecasting_methods():
    aus_production_df = helper.load_data('pysight\\assets\\data\\chapter_5\\aus_production.csv')
    aus_production_df['Quarter_date'] = aus_production_df['Quarter'].apply(helper.quarter_to_datetime)

    aus_production_df.set_index('Quarter', inplace = True)
    aus_production_df.drop(columns = ['Unnamed: 0'], inplace = True)
    bricks_df = aus_production_df.loc['1970 Q1' : '2004 Q4']
    bricks_df['mean_bricks'] = np.mean(bricks_df['Bricks'])

    n_periods = 25
    last_date = bricks_df['Quarter_date'].iloc[-1]
    forecast_dates = pd.date_range(start = last_date, periods = n_periods, inclusive = 'right', freq = 'QS')
    forecast_df = pd.DataFrame(forecast_dates, columns = ['Quarter_date'])
    forecast_df['mean_bricks'] = np.min(bricks_df['mean_bricks'])
    forecast_df['Quarter'] = forecast_df['Quarter_date'].apply(helper.datetime_to_quarter)
    forecast_df.set_index('Quarter', inplace = True)

    # Plot bricks with mean line
    plt.figure(figsize = (12, 7))
    sns.lineplot(data = bricks_df, x = bricks_df.index, y = 'Bricks', color = 'black')
    sns.lineplot(data = bricks_df, x = bricks_df.index, y = 'mean_bricks', color = 'blue', linestyle = '--')
    sns.lineplot(data = forecast_df, x = forecast_df.index, y = 'mean_bricks', color = 'blue')
    plt.title('Mean Forecast')
    ticks = plt.xticks()[0]
    plt.xticks(ticks[::10])
    plt.tight_layout()
    plt.show()

    # Naive method
    plt.figure(figsize = (12, 7))
    forecast_df['naive_bricks'] = bricks_df['Bricks'].iloc[-1]
    sns.lineplot(data = bricks_df, x = bricks_df.index, y = 'Bricks', color = 'black')
    sns.lineplot(data = forecast_df, x = forecast_df.index, y = 'naive_bricks', color = 'blue')
    plt.title('Naive Forecast')
    plt.xticks(ticks[::10])
    plt.tight_layout()
    plt.show()

    # Seasonal Naive method
    def seasonal_naive_forecast(series, seasonal_period):
        return series.tail(seasonal_period)

    forecast = seasonal_naive_forecast(bricks_df['Bricks'], 4)
    forecast = pd.concat([forecast, forecast, forecast, forecast, forecast, forecast])
    forecast_df['seasonal_naive_bricks'] = forecast.values

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

