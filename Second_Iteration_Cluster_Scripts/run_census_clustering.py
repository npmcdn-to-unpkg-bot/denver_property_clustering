import pandas as pd
import numpy as np
import psycopg2
import os
import datetime
import generate_census_data
import generate_parcels_data
import sys
from sklearn.preprocessing import Imputer, StandardScaler
from sklearn.cluster import KMeans, AgglomerativeClustering

"""This script gathers data concerning denver property level characteristics and runs two stage clustering for each month from 01-01-2010 through 12/01/2014.

Author: Michael G Bennett
Create Date: 07/25/2016
Last Update: 07/28/2016

"""

# def kmeans_group(x):
#     """Initial clustering algo groups feature set into 100 clusters. The cluster centers and lable to cluster mappings are then sent to the the agglomerative algo"""
#
#     kmeans_cluster = KMeans(n_clusters=100,n_init=10,random_state=1)
#     kmeans_cluster.fit(x)
#     K_centers = kmeans_cluster.cluster_centers_
#     Kmeans_cluster_mapping = {case: cluster for case, cluster in enumerate(kmeans_cluster.labels_)}
#     print kmeans_cluster.labels_
#     return K_centers, Kmeans_cluster_mapping

def hierarchical_group(X):
    agglomerative_cluster = AgglomerativeClustering(n_clusters=10,affinity='cosine',linkage='complete')
    agglomerative_cluster.fit(X)
    labels =  agglomerative_cluster.labels_
    return labels

def missing_val_imputer(df):
    """Missing values in the final dataframe are imputed using the mean of the column. Missing values are almost exclusivly parcel level metris"""

    imr = Imputer(missing_values="NaN",strategy='mean',axis=0)
    imr = imr.fit(df)
    imputed_data = imr.transform(df.values)
    return imputed_data

def fix_data(df):
    """The is a general clean-up function that drops certain columns, pops parcel_ids and calls the imputer function"""

    # df = df.drop('tax_dist',axis=1)

    # df['prop_class'] = np.where(df['prop_class'].isnull() == True, 0, df['prop_class'])
    # df = df.drop('Unnamed: 0',axis=1)
    df = df.drop('monthd',axis=1)
    df = df.drop('census_tract', axis=1)
    # df = df.drop('pin', axis=1)
    ids = df.pop('tract_date')

    df_final = missing_val_imputer(df)
    X = df_final
    return X, ids

def run_clustering():
    """Main function used for running two-stage clustering. The script calls a previously generated csv with census data (generated via 'generate_census_data.py') and calls generate_census_data.py for the particular months in question. Results are written to the Denver Postgres DB

    This function is called via 'interate_clusters.py'
    """

    ## Call all census data
    # census_df = generate_census_data.run_census_generation()
    census_df = pd.read_csv('census_df.csv')
    census_df['monthd'] = pd.to_datetime(census_df['monthd'])
    census_df = census_df.dropna(axis=1, how='all')
    census_df = census_df.fillna(value=np.nan)

    df_for_clustering = census_df

    df_for_clustering["tract_date"] = df_for_clustering["monthd"].map(str) + df_for_clustering["census_tract"].map(str)

    X, ids = fix_data(df_for_clustering)
    print 'fit'
    stdsc = StandardScaler()
    x = stdsc.fit_transform(X)

    agglom_labels = hierarchical_group(x)
    print 'agglom'


    db_password = os.environ['AWS_DENVER_POSTGRES']
    conn = psycopg2.connect(database='denver', user='postgres', password=db_password,
            host='denverclustering.cfoj7z50le0s.us-east-1.rds.amazonaws.com', port='5432')
    cur = conn.cursor()

    for i in enumerate(agglom_labels):
        cur.execute("insert into cluster_groupings (pin_date, cluster_num,model_run) values (%s,%s, 3);", (ids[i[0]],i[1]))
        conn.commit()

    cur.close()
    conn.close()

if __name__ == '__main__':
    run_clustering()
