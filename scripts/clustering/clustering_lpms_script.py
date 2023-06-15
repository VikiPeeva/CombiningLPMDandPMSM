import pandas as pd
import numpy as np

from sklearn.cluster._agglomerative import AgglomerativeClustering
from sklearn.cluster._dbscan import DBSCAN

from sklearn_extra.cluster import KMedoids


def cluster_hierarchical(distances, linkage, n_clusters=None, distance_threshold=None):
    model = AgglomerativeClustering(metric='precomputed', 
                                    linkage=linkage, 
                                    n_clusters=n_clusters,
                                    distance_threshold=distance_threshold)
    y = model.fit_predict(distances)
    return y
      
    
def cluster_hierarchical_systematically_multiple_measures(distance_measure_dict):
    res = {}
    # iterate all possible distance metrics
    for original_distance_measure, original_distances in distance_measure_dict.items():
        res_measure = cluster_hierarchical_systematically_one(original_distances)
        res = res | {(k[0], k[1], original_distance_measure): v for (k, v) in res_measure.items()}
    return res


def cluster_hierarchical_systematically_one(distances):
    res = {}
    # iterate different parameters systematically
    for linkage in ['single', 'complete', 'average']:
        # for distance_threshold in np.linspace(0.1, 1, 10):
        distance_threshold = None
        num_clusters = None
        # for num_clusters in np.linspace(2, 10, 9, dtype=int):
        for distance_threshold in np.linspace(0.1, 1, 10):
            distance_threshold = round(distance_threshold, 1)
            y = cluster_hierarchical(distances.to_numpy(), linkage, n_clusters=num_clusters, distance_threshold=distance_threshold) # cluster
            df_clust = pd.DataFrame({"Nets": distances.index, "Labels": y})  # concatenate clusters to nets
            # res[(linkage, distance_threshold)] = df_clust
            res[(linkage, num_clusters, distance_threshold)] = df_clust
    return res

                
def cluster_dbscan_systematically(distance_metric_dict):
    # iterate all possible distance metrics
    for original_distance_metric, original_distances in distance_metric_dict.items():
        distances = original_distances
        # iterate different parameters systematically
        for eps in np.linspace(0.1,1,10):
            for min_samples in np.arange(300, 700, 100, dtype=int):
                model = DBSCAN(metric='precomputed',
                               eps=eps,
                               min_samples=min_samples)
                y = model.fit_predict(distances)

                print("====CLUSTERING DONE====")
                df_clust = pd.DataFrame({"Nets": original_distances.index, "Labels": y}) # concatenate clusters to nets
                df_clust.to_csv("results/clustering/phase5/clustering_dbscan_{eps}_{min_samples}_{metric}.csv"
                                .format(eps=eps, min_samples=min_samples, metric=original_distance_metric))
                
                
def cluster_kmedoids_systematically(distance_metric_dict):
    # iterate all possible distance metrics
    for original_distance_metric, original_distances in distance_metric_dict.items():
        distances = original_distances
        # iterate different parameters systematically
        for n in np.arange(10,300,10, dtype=int):
#             for min_samples in np.arange(300, 700, 100, dtype=int):
            model = KMedoids(n_clusters=n,
                             metric='precomputed')
            y = model.fit_predict(distances)

            print("====CLUSTERING DONE====")
            df_clust = pd.DataFrame({"Nets": original_distances.index, "Labels": y}) # concatenate clusters to nets
            df_clust.to_csv("results/clustering/phase6/clustering_medoids_{n_clusters}_{metric}.csv"
                            .format(n_clusters=n, metric=original_distance_metric))
                                

if __name__ == '__main__':
    metric_keys = ["ftd", "nd", "tld", "efg"]
    metric_files = ["model_full_trace_matching_distances.csv", "model_full_trace_matching_distances.csv", "model_full_trace_matching_distances.csv", "model_efg_distances.csv"]
    distance_metric_dict = {}
    for mkey, mfile in zip(metric_keys, metric_files):
        df_distance = pd.read_csv("results/distances/"+mfile, index_col=0).fillna(1)
        distance_metric_dict[mkey] = df_distance

    res = cluster_hierarchical_systematically_multiple_measures(distance_metric_dict)

    for key in res:
        linkage = key[0]
        distance_threshold = key[1]
        measure = key[2]
        df_clust = res[key]
        df_clust.to_csv("results/clustering/clustering_hierarchical_{linkage}_{threshold}_{measure}.csv"
                        .format(linkage=linkage, threshold=distance_threshold, measure=measure))
