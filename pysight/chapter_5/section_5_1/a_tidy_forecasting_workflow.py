import pandas as pd 
import numpy as np
import statsmodels.api as sm
import matplotlib.pyplot as plt
import seaborn as sns
import os 
from ... import helper

def a_tidy_forecasting_workflow():

    # Load data
    gdppc = helper.load_data('pysight\\assets\\data\\chapter_5\\global_economy.csv')
    gdppc['Year'] = pd.to_datetime(gdppc['Year'].astype(str) + '-12-31')
    gdppc['GDP_per_capita'] = gdppc['GDP'] / gdppc['Population']

    plt.figure(figsize = (10, 6))
    sns.lineplot(data = gdppc[gdppc['Country'] == 'Sweden'], x = 'Year', y = 'GDP_per_capita')
    plt.title('GDP per capita for Sweden')
    plt.ylabel('$US')
    plt.show()

    sweden_data = gdppc[gdppc['Country'] == 'Sweden'].copy()
    sweden_data.reset_index(drop = True, inplace = True)
    sweden_data['trend'] = np.arange(len(sweden_data))
    print('Sweden Dataset:', sweden_data.head())

    X = sm.add_constant(sweden_data['trend'])
    y = sweden_data['GDP_per_capita']

    model = sm.OLS(y, X)
    fit = model.fit()

    print('Model summary:', fit.summary())

    n_periods = 3
    forecast_trend = np.arange(len(sweden_data), len(sweden_data) + n_periods)
    forecast_df = pd.DataFrame({'trend' : forecast_trend})
    forecast_df = sm.add_constant(forecast_df)
    predicted_gdp_per_capita = fit.predict(forecast_df)

    print('Predicted GDP per Capita:\n', predicted_gdp_per_capita)

    # Forecast chart without CI
    last_date = sweden_data['Year'].iloc[-1]
    forecast_dates = pd.date_range(start = last_date, periods = n_periods + 1, inclusive = 'right', freq = 'Y')

    plt.figure(figsize = (12, 7))
    plt.plot(sweden_data['Year'], sweden_data['GDP_per_capita'], label = 'Historical Data', color = 'blue')
    plt.plot(forecast_dates, predicted_gdp_per_capita, label = 'Forecast', color = 'red', linestyle = '--')
    plt.title('GDP per capita for Sweden: Historical & Forecasted')
    plt.xlabel('Year')
    plt.ylabel('GDP per capita ($US)')
    plt.legend()
    plt.grid(True)
    plt.show()

    # Forecast chart with CI
    forecast = fit.get_prediction(forecast_df)
    conf_int_80 = forecast.conf_int(alpha = 0.20)
    conf_int_95 = forecast.conf_int(alpha = 0.05)

    plt.figure(figsize = (12, 7))
    plt.plot(sweden_data['Year'], sweden_data['GDP_per_capita'], label = 'Historical Data', color = 'blue')
    plt.plot(forecast_dates, predicted_gdp_per_capita, label = 'Forecast', color = 'red', linestyle = '--')
    plt.fill_between(forecast_dates, conf_int_80[:, 0], conf_int_80[:, 1], color = 'red', alpha = 0.3, label = '80% CI')
    plt.fill_between(forecast_dates, conf_int_95[:, 0], conf_int_95[:, 1], color = 'red', alpha = 0.1, label = '95% CI')
    plt.title('GDP per capita for Sweden with Confidence Intervals')
    plt.xlabel('Year')
    plt.ylabel('GDP per capita ($US)')
    plt.legend()
    plt.grid(True)
    plt.show()
