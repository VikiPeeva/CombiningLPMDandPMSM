import pandas as pd
import os
import sys
import multiprocessing, tqdm

import pm4py

from promosim.algo.measures.structural import ged_normalized_distance_graphs
from promosim.utils.lpms import get_graph_from_petri_net, get_petri_net_place_short_string


def counted(f):
    def wrapped(*args, **kwargs):
        wrapped.calls += 1
        #         if wrapped.calls % 10 == 0:
        print(wrapped.calls)
        return f(*args, **kwargs)

    wrapped.calls = 0
    return wrapped


def counted_calculation(g1, g2, pm_dists=None, place_ss=None):
    return ged_normalized_distance_graphs(g1, g2)  # , pmc=lambda p1, p2: pm_dists[place_ss[p1]][place_ss[p2]], timeout=1)


def ged(name1, name2, graphs):
    g1 = graphs[name1]
    g2 = graphs[name2]
    value = counted_calculation(g1, g2)  # , pm_dists, place_ss)
    if value is None: print("Value none")
    return value


if __name__ == '__main__':
    lpms_file = sys.argv[1]
    res_directory = sys.argv[2]

    # importing the nets
    nets = {}
    graphs = {}
    for file in os.listdir(lpms_file):
        if file.endswith("pnml"):
            nets[file] = pm4py.read_pnml(lpms_file + "/" + file)[0]
            graphs[file] = get_graph_from_petri_net(nets[file])

    print("Import and transformation finished")

    # place_ss = dict(
    #     [(p, get_petri_net_place_short_string(p)) for p in [p1 for net in nets.values() for p1 in net.places]])
    # ss_place = dict([(ss, p) for p, ss in place_ss.items()])
    # pm_dists = {}
    # for p1 in ss_place.keys():
    #     pm_dists[p1] = {}
    #     for p2 in ss_place.keys():
    #         pm_dists[p1][p2] = place_gain_cost(ss_place[p1], ss_place[p2])
    #
    # print("Place matching calculated")

    df_res = pd.DataFrame(columns=nets.keys(), index=nets.keys())

    pool = multiprocessing.Pool(processes=10)
    inputs = []
    visited = set()
    for name1, g1 in graphs.items():
        for name2, g2 in graphs.items():
            if name2 in visited:
                continue
            else:
                inputs.append((name1, name2, graphs))
        visited.add(name1)
    print(len(inputs))
    outputs = pool.starmap(ged, tqdm.tqdm(inputs, total=len(inputs)))
    print(outputs)

    for inp, outp in zip(inputs, outputs):
        df_res[inp[0]][inp[1]] = outp
        df_res[inp[1]][inp[0]] = outp

    df_res.to_csv(res_directory + "/model_ged_distances.csv")
