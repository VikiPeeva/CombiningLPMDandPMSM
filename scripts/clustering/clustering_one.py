import os
import sys

import pandas as pd

from clustering_lpms_script import cluster_hierarchical_systematically_one


if __name__ == '__main__':
    measure = sys.argv[1]
    distances_file = os.path.abspath(sys.argv[2])
    res_directory = os.path.abspath(sys.argv[3])

    # cluster
    df_distance = pd.read_csv(distances_file, index_col=0).fillna(1)
    res = None
    res = cluster_hierarchical_systematically_one(df_distance)
    # try:
    #
    # except Exception:
    #     print(measure)
    #     print(distances_file)

    # save clustering results
    for key in res:
        linkage = key[0]
        num_clusters = key[1]
        if num_clusters is None:
            num_clusters = key[2]
        df_clust = res[key]
        df_clust.to_csv(res_directory + "/clustering_hierarchical_{linkage}_{threshold}_{measure}.csv"
                        .format(linkage=linkage, threshold=num_clusters, measure=measure))

