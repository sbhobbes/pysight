import pandas as pd 
import os 
from statsmodels.tsa.seasonal import seasonal_decompose
import seaborn as sns 
import matplotlib.pyplot as plt 
import calendar
from datetime import datetime
from .... import helper

def seasonal_plots():

    # Load data
    a10_df = helper.load_data('pysight\\fpp3\\assets\\data\\chapter_2\\a10.csv')
    a10_df['Date'] = [datetime.strptime(x, '%Y %b') for x in a10_df['Month']]
    a10_df['Month'] = a10_df['Date'].dt.month
    a10_df['Year'] = a10_df['Date'].dt.year

    # Plot yearly seasons
    plot_df = a10_df.pivot(index = 'Month', columns = 'Year', values = 'Cost')
    plt.figure(figsize = (12, 7))
    for column in plot_df.columns:
        plt.plot(plot_df.index, plot_df[column], label = column)
    plt.title('Seasonal plot: Antidiabetic drug sales')
    plt.ylabel('$ (millions)')
    plt.grid(False)
    plt.legend(title = 'Year', loc = 'upper right')
    plt.xticks(ticks = range(1, 13), labels = list(calendar.month_abbr[1:]))
    plt.show()

    # Load data
    vic_elec_df = helper.load_data('pysight\\fpp3\\assets\\data\\chapter_2\\vic_elec.csv', ['Time'])
    vic_elec_df['Hour'] = vic_elec_df['Time'].dt.hour
    vic_elec_df['Day'] = vic_elec_df['Time'].dt.date

    aggregated_demand = vic_elec_df.groupby(['Hour', 'Day'])['Demand'].mean().reset_index()

    plt.figure(figsize = (12, 7))
    sns.lineplot(data = aggregated_demand, x = 'Hour', y = 'Demand', hue = 'Day')
    plt.title('Electricity demand: Victoria')
    plt.ylabel('MWh')
    plt.xlabel('Time')
    plt.grid(False)
    plt.legend().set_visible(False)
    plt.show()

def daily_plot():
    vic_elec_df = helper.load_data('pysight\\fpp3\\assets\\data\\chapter_2\\vic_elec.csv', ['Time'])
    vic_elec_df['Hour'] = vic_elec_df['Time'].dt.hour
    vic_elec_df['Day'] = vic_elec_df['Time'].dt.date

    aggregated_demand = vic_elec_df.groupby(['Hour', 'Day'])['Demand'].mean().reset_index()

    plt.figure(figsize = (12, 7))
    sns.lineplot(data = aggregated_demand, x = 'Hour', y = 'Demand', hue = 'Day')
    plt.title('Electricity demand: Victoria')
    plt.ylabel('MWh')
    plt.xlabel('Time')
    plt.grid(False)
    plt.legend().set_visible(False)
    plt.show()
