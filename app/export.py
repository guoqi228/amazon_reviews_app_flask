import numpy as np
import pandas as pd
import os

def export_csv(df, asin):
    filename = asin + '.csv'
    outpath = os.path.abspath(os.path.dirname(__file__)) + '/static/csv/' + filename
    df.to_csv(outpath)
