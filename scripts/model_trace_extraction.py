import pandas as pd
import os
import sys

import pm4py
from pm4py.objects.petri_net.obj import Marking

from promosim.utils.lpms import limit_lpm
from promosim.utils.utils import playout_traces


def remap_trace(trace, activity_mapping):
    remapped_trace = []
    for act in trace:
        if act not in activity_mapping:
            activity_mapping[act] = len(activity_mapping)
        remapped_trace.append(activity_mapping[act])
    return remapped_trace


if __name__ == '__main__':
    res_table = pd.DataFrame(columns = ["File name",
                                        "Net string",
                                        "Traces"])
    
    lpms_directory = sys.argv[1]
    res_directory = sys.argv[2]

    print("here")

    activity_mapping = {}
    
    for file in os.listdir(lpms_directory):
        if file.endswith("pnml"):
            net = pm4py.read_pnml(lpms_directory + "/" + file)
            lnet = limit_lpm(net[0], Marking(), Marking())
            traces = playout_traces(*lnet)
            # simpler_mapping = [remap_trace(t, activity_mapping) for t in traces]
            row = [file, net, traces]
            res_table.loc[len(res_table)] = row
            
    res_table.to_csv(res_directory + "/model_traces.csv")
