from __future__ import print_function, division, absolute_import
import sys
import os
import numpy as np
import matplotlib.pyplot as plt
from scipy.optimize import curve_fit
from fio import smart_load_data, dump_results


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


def plot_data(data, popt, meta_info, figname=None):
    fig = plt.figure(figsize=(8, 8), dpi=80)

    # plot the raw data
    plt.subplot(211)
    plt.plot(data[:, 0], data[:, 1], label="Device Data")
    plt.xlabel("V")
    plt.ylabel("J")
    maxy = max(abs(data[:, 1]))
    minx = min(data[:, 0])
    plt.text(minx, maxy*0.9, "file: %s" % meta_info["file"], size=8)
    plt.text(minx, maxy*0.8, "gate: %s" % meta_info["gate"], size=8)
    plt.ylim([-maxy, maxy])
    plt.grid()
    plt.title("Device Measurement")
    plt.legend(loc=4)

    # plot the fitted data
    # global xmax
    # xmax = max(data[:, 0])
    xs_ratio = data[:, 0] / xmax
    ys_ratio = data[:, 1] / (data[-1, 1] - data[0, 1]) * 2.0
    plt.subplot(212)
    plt.plot(data[:, 0], ys_ratio, label="ratio data")
    ys_syn = []
    for x in xs_ratio:
        ys_syn.append(ratio(x, popt[0], popt[1]))
    plt.plot(data[:, 0], ys_syn, linewidth=5, label="fitted data")

    r_square = calculate_r_square(ys_ratio, ys_syn)
    print("r square value: %f" % r_square)
    plt.grid()
    maxy = max(abs(ys_ratio))
    minx = np.min(data[:, 0])
    plt.text(minx, maxy*0.9, "phi0: %.2f eV" % popt[0])
    plt.text(minx, maxy*0.8, "s: %.2f nm" % (get_s(popt[1])*10**9))
    plt.text(minx, maxy*0.7, "r^2: %.3f" % r_square)
    plt.legend(loc=4)
    plt.ylim([-maxy, maxy])
    plt.tight_layout()
    plt.title("Fitting Curve")

    if figname is None:
        plt.show()
    else:
        plt.savefig(figname)

    plt.close(fig)
    return r_square


def get_s(c):
    m = 9.11 * (10 ** -31)
    e = 1.6 * (10 ** -19)
    h = 6.63 * (10 ** -34)
    s = c / np.sqrt(2 * m * e) * h / (4 * np.pi)
    return s


def calculate_r_square(data, data_syn):
    ssres = np.sum(np.power(data - data_syn, 2))
    sstot = np.sum(np.power(data - np.mean(data), 2))
    return (1 - ssres/sstot)


def fit_one_gate(data, meta_info, figname=None):
    global xmax
    xmax = max(data[:, 0])
    xs_ratio = data[:, 0] / xmax
    ys_ratio = data[:, 1] / ((data[-1, 1] - data[0, 1])/2.0)
    try:
        popt, pcov = curve_fit(ratio, xs_ratio, ys_ratio,
                               method="trf",
                               p0=[3, 20])
        print("C2: %f -- C3: %f" % (popt[0], popt[1]))
        print("phi0: %e eV -- s: %e" % (popt[0], get_s(popt[1])))
        print("Covariance Matrix:")
        print(pcov)
    except Exception as err:
        popt = [0, 0]
        print("Error due to: %s" % err)

    try:
        r = plot_data(data, popt, meta_info, figname=figname)
    except Exception as err:
        r = 0.0
        print("Can't plot figure due to: %s" % err)

    return popt[0], get_s(popt[1]), r


def remove_shift(data):
    print(data)
    dist = np.abs(data[:, 0])
    idx = np.argmin(dist)
    shift = data[idx, 1]
    print("remove shift: %f" % shift)
    data[:, 1] = data[:, 1] - shift
    return data
    


def fit_one_file(datafile, rshift=True, outputdir=None):
    print("=" * 30)
    print("Data file: %s" % datafile)
    data, megasweep = smart_load_data(datafile)
    print("Megasweep file: %s" % megasweep)

    if outputdir is not None:
        if not os.path.exists(outputdir):
            os.makedirs(outputdir)

    results = {}
    if megasweep:
        gates = data.keys()
        gates.sort()
        for gate in gates:
            print("-" * 10)
            print("Working on gate: %5.1f" % gate)
            meta = {"file": datafile, "gate": gate}
            if outputdir is not None:
                figname = os.path.join(
                    outputdir, "%s_gate%s.png" % (os.path.basename(datafile),
                                                  gate))
                print("Output figname: %s" % figname)
            else:
                figname = None
            data[gate] = remove_shift(data[gate])
            results[gate] = fit_one_gate(data[gate], meta, figname)
    else:
        print("Output dir: %s" % outputdir)
        meta = {"file": datafile, "gate": 0}
        if outputdir is not None:
            figname = os.path.join(
                outputdir, "%s.png" % (os.path.basename(datafile)))
        else:
            figname = None
        print("shape", data.shape)
        remove_shift(data)
        results[0] = fit_one_gate(data, meta, figname)

    logfile = datafile + ".log"
    print("logfile: %s" % logfile)
    dump_results(results, logfile)


if __name__ == "__main__":

    if len(sys.argv) != 2:
        raise ValueError("Missing input filename")

    fit_one_file(sys.argv[1], rshift=True)
