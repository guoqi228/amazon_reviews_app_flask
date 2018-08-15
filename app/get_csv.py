import pandas as pd
import os

my_path = os.path.abspath(os.path.dirname(__file__))

def get_csv_file(filename):
    url = my_path + '/static/csv/' + filename
    print('url:'.format(url))
    reviews_df = pd.read_csv(url, index_col=0)
    return reviews_df
