from __future__ import print_function, division, absolute_import
import sys
import os
import numpy as np
import matplotlib.pyplot as plt
from scipy.optimize import curve_fit
from fio import smart_load_data, dump_results


def plot_megasweep(data, text="", figname=None):
    print("in plot: %s" % figname)
    gates = data.keys()
    gates.sort()
    for gate in gates:
        plt.plot(data[gate][:, 0], data[gate][:, 1], label="%d" % gate)
    #plt.legend()
    minx = min(data[gate][:, 0])
    ax = plt.gca()
    _, maxy = ax.get_ylim()
    plt.text(minx, maxy*0.9, "source: %s" % text, fontsize=8)
    plt.grid()

    if figname is None:
        plt.show()
    else:
        plt.savefig(figname)

    plt.close('all')
