import pandas as pd
import numpy as np
from sklearn.preprocessing import Imputer, StandardScaler
from sklearn.cluster import KMeans

class KMeans_model(object):
    """

    """
    def __init__(self, month_date):
        self.model = model_class()
        self.grid_search_dict = grid_search_dict



    stdsc = StandardScaler()
    x = stdsc.fit_transform(X)
    print 'scaled x'
    km = KMeans(n_clusters=3,init='random',n_init=10,max_iter=300,tol=1e-04,random_state=0)
    y_km = km.fit(x)
