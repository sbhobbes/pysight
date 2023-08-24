import pandas as pd 
import os 
from statsmodels.tsa.seasonal import seasonal_decompose
import seaborn as sns 
import matplotlib.pyplot as plt 
import calendar
from datetime import datetime

# Load data
current_directory = os.getcwd()
relative_path = 'assets\\data\\chapter_2\\a10.csv'
file_path = os.path.join(current_directory, relative_path)
a10_df = pd.read_csv(file_path)
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
plt.grid(True)
plt.legend(title = 'Year', loc = 'upper right')
plt.xticks(ticks = range(1, 13), labels = list(calendar.month_abbr[1:]))
plt.show()

# Load data
relative_path = 'assets\\data\\chapter_2\\vic_elec.csv'
file_path = os.path.join(current_directory, relative_path)
vic_elec_df = pd.read_csv(file_path, parse_dates = ['Time'])
# vic_elec_df[vic_elec_df[['Time']].duplicated()]

# vic_elec_df.set_index('Time', inplace = True)
# vic_elec_df.drop(columns = ['Unnamed: 0'], inplace = True)
# vic_elec_df['Day'] = vic_elec_df['Time'].dt.date
# vic_elec_df['Time'] = str(vic_elec_df['Time'].dt.hour) + ':' + str(vic_elec_df['Time'].dt.minute)
# sns.lineplot(data = vic_elec_df, x = 'Time', y = 'Demand', hue = 'Day')
# vic_elec_df.drop_duplicates(subset = ['Time'], keep = False, inplace = True)
# plot_df = vic_elec_df.pivot(index = 'Time', columns = 'Day', values = 'Demand')
# print(vic_elec_df)
# plt.figure(figsize = (12, 7))
# for column in plot_df.columns:
#     plt.plot(plot_df.index, plot_df[column])
# plt.title('Electricity demand: Victoria')
# plt.ylabel('MWh')
# plt.grid(True)
# plt.legend(loc = None)
# plt.xticks(ticks = range(1, 25), labels = list(calendar.timegm))
# plt.show()

vic_elec_df['Day'] = vic_elec_df['Time'].dt.date

# Group by day and average (if multiple years are present)
# daily_avg = vic_elec_df.groupby('Day')['Demand'].mean()

# Plotting
plt.figure(figsize=(10, 6))
sns.lineplot(data = vic_elec_df, x = vic_elec_df['Time'].dt.hour, y = 'Demand', hue = 'Day')
plt.title("Electricity demand: Victoria")
plt.ylabel("MWh")
plt.xlabel("Time")
plt.grid(True)
plt.legend().set_visible(False)  # Hide legend

plt.show()
