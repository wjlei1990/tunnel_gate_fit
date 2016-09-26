from __future__ import print_function, division
import sys
import numpy as np


def load_txt_data(filename):
    return np.loadtxt(filename)


def parse_megasweep(data):
    """
    Parse data for mega-sweep
    """
    gate_data = {}
    current_gate = data[0, 2]
    start_idx = 0
    for cidx, val in enumerate(data):
        if val[2] != current_gate:
            gate_data[current_gate] = data[start_idx:cidx]
            current_gate = val[2]
            start_idx = cidx
    gate_data[current_gate] = data[start_idx:]
    return gate_data


def smart_load_data(filename):
    data = load_txt_data(filename)
    if data.shape[1] == 3:
        data = parse_megasweep(data)
        megasweep = True
    elif data.shape[1] == 2:
        megasweep = False

    # filter data from [-0.3, 0.3]
    # for irow, val in enumerate(data[:, 0]):
    #    if val > -0.6:
    #        idx_start = irow
    #        break

    # for irow, val in enumerate(data[:, 0]):
    #    if val > 0.6:
    #        idx_end = irow
    #        break

    # return data[idx_start:idx_end], megasweep
    return data, megasweep


def dump_results(results, logfile):
    with open(logfile, 'w') as fh:
        gates = results.keys()
        gates.sort()
        for gate in gates:
            fh.write("%6.1f %10.3f %10.3f %10.3f\n" %
                     (gate, results[gate][0], results[gate][1] * (10**9),
                      results[gate][2]))
