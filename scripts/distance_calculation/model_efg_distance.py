import pandas as pd
import sys

from promosim.algo.measures.behavioral import efg_similarity_traces

from ast import literal_eval


def get_distance(net_names, df_traces):
    df_res = pd.DataFrame(columns=net_names, index=net_names)

    for net1 in net_names:
        trace_str1 = df_traces.loc[df_traces["File name"] == net1]["Traces"].values[0]
        if trace_str1 == "set()":
            traces1 = set()
        else:
            traces1 = literal_eval(trace_str1)
        for net2 in net_names:
            trace_str2 = df_traces.loc[df_traces["File name"] == net2]["Traces"].values[0]
            if trace_str2 == "set()":
                traces2 = set()
            else:
                traces2 = literal_eval(trace_str2)
            df_res[net1][net2] = efg_similarity_traces(traces1, traces2)
    return 1 - df_res


if __name__ == '__main__':
    trace_file = sys.argv[1]
    res_directory = sys.argv[2]

    df_traces = pd.read_csv(trace_file)
    net_names = df_traces["File name"].unique()

    df_res = get_distance(net_names, df_traces)

    df_res.to_csv(res_directory + "/model_efg_distances.csv")
