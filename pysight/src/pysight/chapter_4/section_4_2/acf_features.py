from statsmodels.tsa.stattools import acf
import pandas as pd 
import numpy as np 
import os 
from pysight.src.pysight import helpers

def acf_features():

    # Load data
    tourism_df = helpers.load_data('pysight\\fpp3\\assets\\data\\chapter_4\\tourism.csv')

    def compute_acf_features(group):
        trips = group['Trips'].values

        acf_values = acf(trips, nlags = 10, fft = True)
        acf1 = acf_values[1]
        acf10 = acf_values[10]

        diff1_acf_values = acf(np.diff(trips, n = 1), nlags = 10, fft = True)
        diff1_acf1 = diff1_acf_values[1]
        diff1_acf10 = diff1_acf_values[10]

        diff2_acf_values = acf(np.diff(trips, n = 2), nlags = 10, fft = True)
        diff2_acf1 = diff2_acf_values[1]
        diff2_acf10 = diff2_acf_values[10]

        season_acf1 = acf_values[4]

        return pd.Series({
            'acf1' : acf1,
            'acf10' : acf10,
            'diff1_acf1' : diff1_acf1,
            'diff1_acf10' : diff1_acf10,
            'diff2_acf1' : diff2_acf1,
            'diff2_acf10' : diff2_acf10,
            'season_acf1' : season_acf1
        })

    features_df = tourism_df.groupby(['Region', 'State', 'Purpose']).apply(compute_acf_features).reset_index()

    print(features_df.head())
