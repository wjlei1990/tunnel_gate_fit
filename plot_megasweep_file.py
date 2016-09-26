import os
import sys
from fio import smart_load_data
from plot_utils import plot_megasweep


def plot_megafile(datafile, outputdir=None):
    print("=" * 30)
    print("Megasweep file: %s" % datafile)
    data, megasweep = smart_load_data(datafile)

    if not megasweep:
        raise ValueError("Not megasweep file")
        return

    plot_megasweep(data, os.path.basename(datafile))


if __name__ == "__main__":

    if len(sys.argv) != 2:
        raise ValueError("Missing input file")

    plot_megafile(sys.argv[1])
