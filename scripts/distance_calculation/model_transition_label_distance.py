import pandas as pd
import os
import sys

import pm4py

from promosim.algo.measures.elementary import transition_label_similarity


if __name__ == '__main__':
    lpms_directory = sys.argv[1]
    res_directory = sys.argv[2]
    
    # importing the nets
    nets = {}
    for file in os.listdir(lpms_directory):
        if file.endswith("pnml"):
            nets[file] = pm4py.read_pnml(lpms_directory + "/" + file)[0]
    
    df_res = pd.DataFrame(columns=nets.keys(), index=nets.keys())
    
    for name1, net1 in nets.items():
        for name2, net2 in nets.items():
            df_res[name1][name2] = transition_label_similarity(net1, net2)

    df_res = 1 - df_res
    df_res.to_csv(res_directory + "/model_transition_label_distances.csv")
