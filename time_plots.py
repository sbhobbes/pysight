import pandas as pd
import matplotlib.pyplot as plt 
import seaborn as sns 
import os 
from .... import helper

def time_plots():
    
    # Load data
    melsyd_economy_df = helper.load_data('pysight\\fpp3\\assets\\data\\chapter_1\\melsyd_economy.csv')

    # Filter the dataset
    melsyd_filter = ((melsyd_economy_df['Airports'] == 'MEL-SYD') & (melsyd_economy_df['Class'] == 'Economy'))
    melsyd_economy_df = melsyd_economy_df[melsyd_filter]
    melsyd_economy_df['Passengers'] = melsyd_economy_df['Passengers'] / 1000
    melsyd_economy_df.set_index('Week')

    # Plot the series
    plt.figure(figsize = (12, 7))
    sns.lineplot(data = melsyd_economy_df, x = melsyd_economy_df.index, y = 'Passengers')
    plt.suptitle('Ansett airlines economy class')
    plt.title('Melbourne-Sydney')
    plt.ylabel('Passeners (\'000)')
    plt.xlabel('Week [1W]')
    plt.show()

    # Load data
    a10_df = helper.load_data('pysight\\fpp3\\assets\\data\\chapter_2\\a10.csv')

    # Plot the series
    plt.figure(figsize = (12, 7))
    a10_df.plot(x = 'Month', y = 'Cost')
    plt.title('Australian antidiabetic drug sales')
    plt.ylabel('$ (millions)')
    plt.tight_layout()
    plt.show()
