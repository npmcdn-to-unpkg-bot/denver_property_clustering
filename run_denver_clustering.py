import pandas as pd
import numpy as np
import psycopg2
import os
import datetime
import data_pipeline
from sklearn.preprocessing import Imputer, StandardScaler
from sklearn.cluster import KMeans, AgglomerativeClustering


def kmeans_group(x):
    kmeans_cluster = KMeans(n_clusters=100,n_init=10,random_state=1)
    kmeans_cluster.fit(x)
    K_centers = kmeans_cluster.cluster_centers_
    Kmeans_cluster_mapping = {case: cluster for case, cluster in enumerate(clustering.labels_)}
    return K_centers, Kmeans_cluster_mapping

def hierarchical_group(K_centers,Kmeans_cluster_mapping):
    agglomerative_cluster = AgglomerativeClustering(n_clusters=10,affinity='cosine',linkage='complete')
    agglomerative_cluster.fit(K_centers)
    agglomerative_mapping = {case:cluster for case, cluster in enumerate(agglomerative_cluster.labels_)}
    final_mapping = {case: agglomerative_mapping[Kmeans_cluster_mapping[case]] for case in Kmeans_cluster_mapping}
    return final_mapping

def missing_val_imputer(df):
    imr = Imputer(missing_values="NaN",strategy='mean',axis=0)
    imr = imr.fit(df)
    imputed_data = imr.transform(df.values)
    return imputed_data

def fix_data(df):
    #do we need to drop census_tract and monthd?????
    df = df.drop('tax_dist',axis=1)
    df['prop_class'] = np.where(df['prop_class'].isnull() == True, 0, df['prop_class'])
    ids = df.pop('gid')
    df_final = missing_val_imputer(df)
    X = df_final
    return X, ids

if __name__ == '__main__':

    db_password = os.environ['AWS_DENVER_POSTGRES']
    conn = psycopg2.connect(database='denver', user='postgres', password=db_password,
            host='denverclustering.cfoj7z50le0s.us-east-1.rds.amazonaws.com', port='5432')
    cur = conn.cursor()
    cur.execute("Select distinct monthd from pin_dates;")

    ## Call all census data
    census_df = generate_census_data.run_census_generation()
    # full_clustering_data = data_pipeline.call_pipeline()
    dict_holder = []
    for i in cur:
        monthd = i[0]
        census_mask = (census_df['monthd'] == monthd)
        monthly_census_df = census_df.loc[mask]
        ## alter this for the monthly data 
        parcels_df = generate_parcels_data.run_parcel_generation()
        df_for_clustering = pd.merge(parcels_df, monthly_census_df, on='census_tract')

        X, ids = fix_data(df_for_clustering)
        stdsc = StandardScaler()
        x = stdsc.fit_transform(X)

        kmeans_centers, kmeans_cluster_mapping = kmeans_group(X)
        agglom_map = hierarchical_group(kmeans_centers, kmeans_cluster_mapping)
        dict_holder.append(agglom_map)
