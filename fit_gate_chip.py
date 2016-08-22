from __future__ import print_function, division
import os
import numpy as np
import matplotlib.pyplot as plt
from scipy.optimize import curve_fit


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
    #for irow, val in enumerate(data[:, 0]):
    #    if val > -0.6:
    #        idx_start = irow
    #        break

    #for irow, val in enumerate(data[:, 0]):
    #    if val > 0.6:
    #        idx_end = irow
    #        break

    #return data[idx_start:idx_end], megasweep
    return data, megasweep


def ratio(tao, c2, c3):
    """
    commonly used, to get phi0(in c2) and s(in c3)
    """
    def func(x, c2, c3):
        term1 = (c2 - x/2.0) * np.exp(- c3 * np.sqrt(c2 - x/2.0))
        term2 = (c2 + x/2.0) * np.exp(- c3 * np.sqrt(c2 + x/2.0))
        return term1 - term2
    x = xmax * tao
    return func(x, c2, c3) / func(xmax, c2, c3)


def ratio_fixed_c2(tao, c3):
    """
    Ratio function with fixed phi0 value
    """
    c2 = 5
    def func1(x, c3):
        term1 = (c2 - x/2.0) * np.exp(- c3 * np.sqrt(c2 - x/2.0))
        term2 = (c2 + x/2.0) * np.exp(- c3 * np.sqrt(c2 + x/2.0))
        return (term1 - term2)
    x = xmax * tao
    return func1(x, c3) / func1(xmax, c3)


def plot_data(data, popt, figname):
    plt.figure(figsize=(10, 10))

    # plot the raw data
    plt.subplot(211)
    plt.plot(data[:, 0], data[:, 1], label="Device Data")
    plt.xlabel("V")
    plt.grid()
    plt.legend(loc=4)

    # plot the fitted data
    # global xmax
    # xmax = max(data[:, 0])
    xs_ratio = data[:, 0] / xmax
    ys_ratio = data[:, 1] / max(data[:, 1])
    plt.subplot(212)
    plt.plot(data[:, 0], ys_ratio, label="ratio data")
    ys_syn = []
    for x in xs_ratio:
        ys_syn.append(ratio(x, popt[0], popt[1]))
    plt.plot(data[:, 0], ys_syn, linewidth=5, label="fitted data")

    plt.grid()
    plt.legend(loc=4)
    plt.show()
    #plt.savefig(figname)


def get_s(c):
    m = 9.11 * 10**-31
    e = 1.6 * 10 **-19
    h = 6.63 * 10**-34
    s = c / np.sqrt(2 * m * e) * h / (4 * np.pi)
    return s


def fit_one_gate(data, outputdir):
    global xmax
    xmax = max(data[:, 0])
    xs_ratio = data[:, 0] / xmax
    ys_ratio = data[:, 1] / max(data[:, 1])
    popt, pcov = curve_fit(ratio, xs_ratio, ys_ratio,
                           method="trf",
                           p0=[3, 20])
    print("C2: %f -- C3: %f" % (popt[0], popt[1]))
    print("phi0: %e eV -- s: %e" % (popt[0], get_s(popt[1])))
    print("Covariance Matrix:")
    print(pcov)

    figname = os.path.join(outputdir, "fit_data.png")
    plot_data(data, popt, figname)


def main(datafile, outputdir):
    data, megasweep = smart_load_data(datafile)
    print("=" * 20)
    print("Data file: %s" % datafile)
    print("Megasweep file: %s" % megasweep)

    if megasweep:
        gates = data.keys()
        gates.sort()
        for gate in gates:
            _dir = os.path.join(outputdir, "gate_%5.1f" % gate)
            if not os.path.exists(_dir):
                os.mkdir(_dir)
            print("="*10)
            print("Working on gate: %5.1f" % gate)
            print("Output dir: %s" % _dir)
            fit_one_gate(data[gate], outputdir)
    else:
        print("Output dir: %s" % outputdir)
        fit_one_gate(data, outputdir)


if __name__ == "__main__":
    datafile = "test_data/05202015_chip9_D4_1-2_300k_10pA_megasweep.dat"
    outputdir = "."
    main(datafile, outputdir)
