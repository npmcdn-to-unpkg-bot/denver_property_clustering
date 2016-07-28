import pandas as pd
import numpy as np
import psycopg2
import os
import generate_census_data

"""This script is used to generate parcel level features on a montly basis.

Data is stored in an AWS RDS Portgres instance and accessed via SQL scripts where noted. These files can be acccessed through the project repo. Otherwise inline queries are used.

Author: Michael G Bennett
Create Date: 07/19/2016
Last Update: 07/26/2016

"""

def load_parcel_dataframe(db_password, month_date):
    """Pulls baseline parcel information. For each month through time, most features remain the same unless remoldes or new construction has occured on the property. In the future or with more time, a more indepth analysis of infrasture change could be done."""

    conn = psycopg2.connect(database='denver', user='postgres', password=db_password,
            host='denverclustering.cfoj7z50le0s.us-east-1.rds.amazonaws.com', port='5432')
    cursor = conn.cursor()

    cursor.execute("Select cast(ltrim(census_tract_name,'Census Tract ') as real) as census_tract, tax_dist, land_value, prop_class, total_valu, land, ccyrblt,sale_price, gid, pin from parcels;")
    parcel_df =pd.DataFrame(cursor.fetchall(),columns=['census_tract','tax_dist', 'land_value','prop_class','total_valu','land','ccyrblt','sale_price','gid','pin'])

    conn.close()
    return parcel_df

def load_spacial_metrics(db_password, month_date):

    conn = psycopg2.connect(database='denver', user='postgres', password=db_password,
            host='denverclustering.cfoj7z50le0s.us-east-1.rds.amazonaws.com', port='5432')
    cursor = conn.cursor()

    cursor.execute("Select sales_count, avg_price, pin from sales_metrics where monthd = %s;",(month_date,))
    spacial_metrics_df =pd.DataFrame(cursor.fetchall(),columns=['sales_count','avg_price', 'pin'])

    conn.close()
    return spacial_metrics_df


def run_parcel_generation(month_date):

    db_password = os.environ['AWS_DENVER_POSTGRES']

    parcel_features_df = load_parcel_dataframe(db_password,month_date)
    spacial_metrics_df = load_spacial_metrics(db_password,month_date)
    final_parcels_df = pd.merge(parcel_features_df, spacial_metrics_df, on='pin')
    final_parcels_df.to_csv('parcels_df.csv')
    return final_parcels_df
