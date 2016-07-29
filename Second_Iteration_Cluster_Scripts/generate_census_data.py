import pandas as pd
import numpy as np
import psycopg2
import os

"""This script is used to iterate census tracts, pulling 4 years of data from the census info. Data is also pivoted from original DB structure.

Author: Michael G Bennett
Create Date: 07/29/2016
Last Update: 07/29/2016

"""

def run_census_generation():
    """For each census tract, pivot and interpolat missing data, return the dataframes to a list and concat to form full censue dataframe"""

    #Establish DB Connection
    db_password = os.environ['AWS_DENVER_POSTGRES']
    conn = psycopg2.connect(database='denver', user='postgres', password=db_password,
            host='denverclustering.cfoj7z50le0s.us-east-1.rds.amazonaws.com', port='5432')
    cursor = conn.cursor()

    #Select Distinct Census Tract Numbers:
    cursor.execute("Select distinct cast(ltrim(tract_name,'Census Tract ') as real) as census_tract from census_tracts;")

    #Load 2010-2014 ACS Annual Survey Data, pivot and interpolate.
    x = 1
    for i in cursor:
        df = load_census_data_by_tract(db_password,i[0])
        pivoted_df = pivot_census_data(df,i[0])
        finaldf = pivoted_df
        # finaldf = linear_interpolation(pivoted_df)
        if x == 1:
            master_df = finaldf
        else:
            master_df = pd.concat([master_df,finaldf])
        x += 1
    master_df['monthd'] = pd.to_datetime(master_df['monthd'])
    master_df.to_csv('census_df.csv')
    return master_df


def load_census_data_by_tract(db_password,census_tract):
    """Pull Census Data for requested tract number"""

    conn = psycopg2.connect(database='denver', user='postgres', password=db_password,
            host='denverclustering.cfoj7z50le0s.us-east-1.rds.amazonaws.com', port='5432')
    cursor = conn.cursor()

    cursor.execute("Select distinct census_code, value, census_tract, p.monthd from (select distinct monthd from pin_dates where monthd = '12/01/2010' or monthd = '12/01/2011' or monthd = '12/01/2012' or monthd = '12/01/2014') p left join (select census_code, value, census_tract, monthd from census_info where census_tract = '%s') ci on p.monthd = ci.monthd;",(census_tract,))
    census_df =pd.DataFrame(cursor.fetchall(),columns=['census_code','value','census_tract', 'monthd'])
    cursor.close()
    conn.close()
    return census_df

def pivot_census_data(unpivoted_dataframe,census_tract):
    """Pivots census dataframe. Month_Date becomes leading column, followed by 136 census measuremetns"""

    pivoted_census_df = unpivoted_dataframe.pivot(index='monthd',columns='census_code',values='value')
    census_dataframe = pivoted_census_df.reset_index()
    census_dataframe['census_tract'] = census_tract
    return census_dataframe

def linear_interpolation(census_dataframe):
    """Census data in the ACS Annual Survey is a single value. For feature engineeer purposes and time contraint limitations, the following decissions were made:
            - Annual data point is applied to December of the given year.
            - Data in 2010 and 2015 is backfilled and forward filled, respectivly
            - Middle years use linear interporation"""

    df10 = census_dataframe[:12]
    df10 = df10.fillna(method='bfill')
    df11 = census_dataframe[11:24]
    df11 = df11.interpolate(method='linear')
    df12 = census_dataframe[23:36]
    df12 = df12.interpolate(method='linear')
    df13 = census_dataframe[35:48]
    df13 = df13.interpolate(method='linear')
    df14 = census_dataframe[47:60]
    df14 = df14.fillna(method='ffill')

    frames = [df10,df11,df12,df13,df14]
    concated_df = pd.concat(frames)
    final_df = concated_df.drop_duplicates()
    return final_df

if __name__ == '__main__':
    run_census_generation()
