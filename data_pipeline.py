import pandas as pd
import numpy as np
import psycopg2
import os
import generate_census_data

"""This script is used as the main data loading and pre-processing file for property level clustering in Denver, CO.

Data is stored in an AWS RDS Portgres instance and accessed via SQL scripts where noted. These files can be acccessed through the project repo. Otherwise inline queries are used.

Author: Michael G Bennett
Create Date: 07/19/2016
Last Update: 07/19/2016

"""

def load_parcel_dataframe(db_password):
    """Pulls baseline parcel information. Returns: Dataframe"""

    conn = psycopg2.connect(database='denver', user='postgres', password=db_password,
            host='denverclustering.cfoj7z50le0s.us-east-1.rds.amazonaws.com', port='5432')

    with conn.cursor() as cursor:
        cursor.execute(open("sql_scripts/parcels_load.sql", "r").read())
        parcel_df =pd.DataFrame(cursor.fetchall(),columns=['census_tract','tax_dist', 'land_value','prop_class','total_valu','land','ccyrblt','sale_month','sale_year','sale_price','gid'])

    conn.close()
    return parcel_df

def call_pipeline():
    db_password = os.environ['AWS_DENVER_POSTGRES']
    parcels_df = load_parcel_dataframe(db_password)
    census_df = generate_census_data.run_census_generation()
    combined_df = pd.merge(parcels_df, census_df, on='census_tract')
    return combined_df
