import pandas as pd
import numpy as np
import psycopg2
import os

"""This script is used as the main data cleaning and feature engineering file for property level clustering in Denver, CO.

Data is fed from the data_pipeline.py script as a dataframe

Author: Michael G Bennett
Create Date: 07/19/2016
Last Update: 07/19/2016

"""

def tax_dist(df):
    df['tax_dist'] = np.where(df['tax_dist'].isnull() == True, 0, df['tax_dist'])

    return df


def prop_class(df):
    df['prop_class'] = np.where(df['tax_dist'].isnull() == True, 0, df['prop_class'])

    return df
