import statsmodels.tsa.seasonal as sts
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
import seaborn as sns
from pysight.src.pysight import helpers

def stl_decomposition():
    # data = pd.read_csv('C:/Users/sbhobbes/Downloads/us_retail_employment.csv', parse_dates = ['Month'], dtype = {'Title' : str, 'Employed' : np.float64})
    data = helpers.load_data('pysight\\fpp3\\assets\\data\\chapter_3\\us_retail_employment.csv', ['Month'])
    data.set_index('Month', inplace = True)

    # Decompose the time series
    decomposition = sts.seasonal_decompose(data['Employed'])

    # Extract the trend component
    trend = decomposition.trend

    # Extract the seasonality component
    seasonality = decomposition.seasonal

    # Extract the noise component
    noise = decomposition.resid

    seasonal_adjust = trend + noise

    fig, ax = plt.subplots(4)
    ax[0].plot(data['Employed'])
    ax[1].plot(trend)
    ax[2].plot(seasonality)
    ax[3].plot(noise)
    plt.tight_layout()
    plt.show()

    #####################################################
    # Alternate:
    decomposition.plot()
    plt.show()
