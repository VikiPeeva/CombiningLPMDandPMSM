import pandas as pd
import sys

from promosim.utils.matching import calculate_optimal_trace_matching

from ast import literal_eval


def counted(f):
    def wrapped(*args, **kwargs):
        wrapped.calls += 1
        if wrapped.calls % 10000 == 0:
            print(wrapped.calls)
        return f(*args, **kwargs)
    wrapped.calls = 0
    return wrapped


@counted
def trace_matching_distance(traces1, traces2):
    cost_matrix, assignment = calculate_optimal_trace_matching(traces1, traces2)
    return 2 * cost_matrix[assignment].sum() / (len(traces1) + len(traces2))


def extract_traces_from_string(trace_str):
    if trace_str == "set()":
        return set()
    else:
        return literal_eval(trace_str)


if __name__ == '__main__':
    trace_file = sys.argv[1]
    res_directory = sys.argv[2]
    
    df_traces = pd.read_csv(trace_file)
    net_names = df_traces["File name"].unique()
    df_res = pd.DataFrame(columns=net_names, index=net_names)
    
    for net1 in net_names:
        trace_str1 = df_traces.loc[df_traces["File name"] == net1]["Traces"].values[0]
        traces1 = extract_traces_from_string(trace_str1)
        for net2 in net_names:
            trace_str2 = df_traces.loc[df_traces["File name"] == net2]["Traces"].values[0]
            traces2 = extract_traces_from_string(trace_str2)
            df_res[net1][net2] = trace_matching_distance(traces1, traces2)

    df_res = 1 - df_res
    df_res.to_csv(res_directory + "/model_full_trace_matching_distances.csv")
    