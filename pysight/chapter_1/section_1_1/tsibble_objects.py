import pandas as pd 
import numpy as np
import os
from ... import helper

# Example of yearly data
def tsibble_samples():
    y = pd.DataFrame(
        {
            'Year' : np.arange(2015, 2020),
            'Observation' : [123, 39, 78, 52, 110]
        }
    )
    y.set_index('Year', inplace = True)

    print('Yearly data:\n', y)

    # Example of monthly data
    z = pd.DataFrame(
        {
            'Month' : pd.date_range('01/01/2019', '05/31/2019', inclusive = 'both', freq = 'M'),
            'Observation' : [50, 23, 34, 30, 25]
        }
    )
    z['Month'] = z['Month'].dt.strftime('%Y %b')
    z.set_index('Month', inplace = True)

    print('Monthly data:\n', z)

    # Key variables
    olympic_running_df = helper.load_data('pysight\\assets\\data\\chapter_1\\olympic_running.csv')

    print('Olympic running data:\n', olympic_running_df.head(10))

    print('Distinct Sex from the Olympic Running data:\n', olympic_running_df['Sex'].unique())

    # Filtering
    pbs_df = helper.load_data('pysight\\assets\\data\\chapter_1\\pbs.csv')

    pbs_filtered_df = pbs_df[pbs_df['ATC2'] == 'A10']
    print('Filtered PBS data:\n', pbs_filtered_df.head(10))

    pbs_filtered_selected_df = pbs_filtered_df[['Month', 'Concession', 'Type', 'Cost']]
    print('Filtered PBS data with specific columns selected:\n', pbs_filtered_selected_df)

    pbs_summarized_df = pbs_filtered_selected_df[['Month', 'Cost']].groupby('Month').sum()
    pbs_summarized_df.columns = ['TotalC']
    print('PBS Data summarized to total cost per month:\n', pbs_summarized_df.head(10))

    pbs_summarized_df['Cost'] = round(pbs_summarized_df['TotalC'] / 1e6, 2)
    print('PBS data mutated:\n', pbs_summarized_df)

    current_directory = os.getcwd()
    relative_path = 'pysight\\assets\\data\\chapter_1\\a10.csv'
    file_path = os.path.join(current_directory, relative_path)
    pbs_summarized_df.to_csv(file_path)
