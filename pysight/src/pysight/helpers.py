import pandas as pd
import os
from importlib import resources


def get_data_from_file(chapter, file):
    with resources.path(chapter, file) as f:
        df = pd.read_csv(f)
    
    return df
    

def load_data(relative_file_path: str, dates_to_parse: list = None):
    
    current_directory = os.getcwd()
    file_path = os.path.join(current_directory, relative_file_path)

    if '.csv' in(relative_file_path):
        if dates_to_parse:
            return pd.read_csv(file_path, parse_dates = dates_to_parse)
        else:
            return pd.read_csv(file_path)
    else:
        print('The chosen file type has not been defined in this function.')

def quarter_to_datetime(quarter_str: str):
    year, q = quarter_str.split(' ')
    quarter_month_map = {
        'Q1' : '01-01',
        'Q2' : '04-01',
        'Q3' : '07-01',
        'Q4' : '10-01'
    }
    return pd.to_datetime(f'{year}-{quarter_month_map[q]}')

def datetime_to_quarter(dt):
    if dt.month <= 3:
        quarter = 'Q1'
    elif dt.month <= 6:
        quarter = 'Q2'
    elif dt.month <= 9:
        quarter = 'Q3'
    else:
        quarter = 'Q4'

    return f'{dt.year} {quarter}'
