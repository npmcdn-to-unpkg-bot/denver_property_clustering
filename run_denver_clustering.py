import pandas as pd
import numpy as np
import psycopg2
import os
import datetime
import data_pipeline
import two_stage_clustering

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
    return agglomerative_mapping

if __name__ == '__main__':

    conn = psycopg2.connect(database='denver', user='postgres', password=db_password,
            host='denverclustering.cfoj7z50le0s.us-east-1.rds.amazonaws.com', port='5432')
    cur = conn.cursor()
    cur.execute("Select distinct monthd from pin_dates;")

    full_clustering_data = data_pipeline.call_pipeline()

    for i in cur:
        monthd = i[0]
        df_for_clustering = np.where(full_clustering_data['monthd']==monthd)
        kmeans_centers, kmeans_cluster_mapping = kmeans_group(df_for_clustering)
        agglom_map = hierarchical_group(kmeans_centers, kmeans_cluster_mapping)
