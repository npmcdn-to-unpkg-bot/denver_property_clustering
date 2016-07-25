from sklearn.preprocessing import Imputer, StandardScaler
from sklearn.cluster import KMeans, AgglomerativeClustering

class Two_Stage_Clustering(object):
    """This class is used to instantiate and run a two stage clustering algorithm.

    Author: Michael G Bennett
    Create Date: 07/23/2016
    Last Update: 07/23/2016

    """
    
    def __init__(self, month_date):
        self.model = model_class()

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
