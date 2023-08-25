import pandas as pd 
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import os 

# Load data
current_directory = os.getcwd()
relative_path = 'assets\\data\\chapter_5\\aus_production.csv'
file_path = os.path.join(current_directory, relative_path)

# Filter and get bricks data
aus_production_df = pd.read_csv('C:/Users/sbhobbes/Downloads/aus_production.csv')
aus_production_df.set_index('Quarter', inplace = True)
aus_production_df.drop(columns = ['Unnamed: 0'], inplace = True)
bricks_df = aus_production_df.loc['1970 Q1' : '2004 Q4']
bricks_df['mean_bricks'] = np.mean(bricks_df['Bricks'])

# Plot bricks with mean line
plt.figure(figsize = (12, 7))
sns.lineplot(data = bricks_df, x = bricks_df.index, y = 'Bricks', color = 'black')
sns.lineplot(data = bricks_df, x = bricks_df.index, y = 'mean_bricks', color = 'blue', linestyle = '--')
plt.tight_layout()
plt.show()

# Naive method
