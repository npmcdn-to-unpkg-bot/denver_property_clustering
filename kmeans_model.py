import pandas as pd
import numpy as np
import psycopg2
from sklearn.preprocessing import Imputer, StandardScaler
from sklearn.cluster import KMeans, AgglomerativeClustering
from data_pipeline import call_pipeline
import matplotlib.pyplot as plt
import seaborn as sbn
import os

def missing_val_imputer(df):
    imr = Imputer(missing_values="NaN",strategy='mean',axis=0)
    imr = imr.fit(df)
    imputed_data = imr.transform(df.values)
    return imputed_data

def fix_data(df):
    df = df.drop('tax_dist',axis=1)
    df['prop_class'] = np.where(df['prop_class'].isnull() == True, 0, df['prop_class'])
    ids = df.pop('gid')
    df_final = missing_val_imputer(df)
    X = df_final
    return X, ids

def kmeans_cluster(x):
    clustering = KMeans(n_clusters=100,n_init=10,random_state=1)
    clustering.fit(x)
    Kx = clustering.cluster_centers_
    Kx_mapping = {case:cluster for case, cluster in enumerate(clustering.labels_)}
    return Kx_mapping


if __name__ == '__main__':

    df = call_pipeline()
    X, ids = fix_data(df)
    stdsc = StandardScaler()
    x = stdsc.fit_transform(X)
    clustering = KMeans(n_clusters=100,n_init=10,random_state=1)
    clustering.fit(x)
    Kx = clustering.cluster_centers_
    Kx_mapping = {case:cluster for case, cluster in enumerate(clustering.labels_)}

    Hclustering = AgglomerativeClustering(n_clusters=10,affinity='cosine',linkage='complete')
    Hclustering.fit(Kx)
    H_mapping = {case:cluster for case,cluster in enumerate(Hclustering.labels_)}
    final_mapping = {case:H_mapping[Kx_mapping[case]] for case in Kx_mapping}

    groupings = []
    for key, value in final_mapping.iteritems():
        groupings.append(value)

    db_password = os.environ['AWS_DENVER_POSTGRES']
    conn = psycopg2.connect(database='denver', user='postgres', password=db_password,
            host='denverclustering.cfoj7z50le0s.us-east-1.rds.amazonaws.com', port='5432')
    cur = conn.cursor()

    for i in enumerate(groupings):
        cur.execute("Update parcels set cluster_num = %s Where gid = %s;", (groupings[i[0]],ids[i[0]]))
        conn.commit()

    cur.close()
    conn.close()
    # km = KMeans(n_clusters=250,init='random',n_init=10,max_iter=10000,tol=1e-04,random_state=0)
    # y_km = km.fit(x)
