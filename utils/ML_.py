####### Utils for ML functions #######

# math-df libraries
import numpy as np
import pandas as pd

# ML libraries
from sklearn.preprocessing import StandardScaler
from sklearn.cluster import KMeans
from sklearn.cluster import DBSCAN

def standardize(data):
    return StandardScaler().fit_transform(data)


def predict(fit, data, *args, **kwargs):
    
    y_pred = fit.predict(data)
    return y_pred

def pred_to_df(y_pred, data):
    
    copy = data.copy(deep=True)
    copy['pred'] = y_pred    
    return copy

################### Algorithms ###############################
def Algo_KMeans(data, n_clusters, *args, **kwargs):
    
    kmeans = KMeans(n_clusters=n_clusters, *args, **kwargs)
    model  = kmeans.fit(data)
    return model

def cluster_number_KMeans(X, max_cluster, *args, **kwargs):
   
    sum_of_squared_distances = []
    K = range(1, max_cluster)
    for n_cluster in K:
        km = Algo_KMeans(X, n_cluster, *args, **kwargs)
        sum_of_squared_distances.append(km.inertia_)
    return sum_of_squared_distances, K
        
def Algo_DBScan(data, epsilon, min_samples, *args, **kwargs):
    
    dbscan = DBSCAN(eps=epsilon, min_samples=min_samples, n_jobs=-1, *args, **kwargs)
    model  = dbscan.fit(data)
    return model