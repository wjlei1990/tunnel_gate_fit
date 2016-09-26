# scripts that runs all the plotting
import os
import glob
from fio import smart_load_data
from plot_utils import plot_megasweep


def plot_megafile(datafile, text, figname):

    data, megasweep = smart_load_data(datafile)

    if not megasweep:
        print("Not a megasweep file")
        return

    plot_megasweep(data, text=text, figname=figname)


def plot1(database, dirname):
    outputbase = os.path.join(database, dirname, "megasweep")
    print("outputbase: %s" % outputbase)
    if not os.path.exists(outputbase):
        os.makedirs(outputbase)

    subdirs = glob.glob(os.path.join(database, dirname, "*"))
    print("subdirs: %s" % subdirs)
    subdirs.sort()
    for subdir1 in subdirs:
        filelist = glob.glob(os.path.join(subdir1, "*.dat"))
        filelist.sort()
        for datafile in filelist:
            print("=" * 20)
            # plot only(no save)
            #fit_one_file(datafile)
            # save plot only
            text = "|--|".join(datafile.split("/")[-2:])
            figname = os.path.join(outputbase, "%s.pdf" % text)
            print("datafile: %s" % datafile)
            print("figname: %s" % figname)
            print("text: %s" % text)
            plot_megafile(datafile, text=text, figname=figname)


def plot2(database, dirname):
    outputbase = os.path.join(database, dirname, "megesweep")
    print("outputbase: %s" % outputbase)
    if not os.path.exists(outputbase):
        os.makedirs(outputbase)

    subdirs = glob.glob(os.path.join(database, dirname, "*"))
    print("subdirs: %s" % subdirs)
    subdirs.sort()
    for subdir1 in subdirs:
        subdirs1 = glob.glob(os.path.join(subdir1, "*"))
        for subdir2 in subdirs1:
            filelist = glob.glob(os.path.join(subdir2, "*.dat"))
            filelist.sort()
            for datafile in filelist:
                print("=" * 20)
                # plot only(no save)
                #fit_one_file(datafile)
                # save plot only
                text = "|--|".join(datafile.split("/")[-3:])
                figname = os.path.join(outputbase, "%s.png" % text)
                print("datafile: %s" % datafile)
                print("figname: %s" % figname)
                print("text: %s" % text)
                plot_megafile(datafile, text=text, figname=figname)


def main(database, dirname):

    if dirname in ["20140526_chip5_tunneling", "20140526_chip6_tunneling"]:
        plot1(database, dirname)
    elif dirname in ["chip9", "chip8_raw_data_Q"]:
        plot2(database, dirname)
    else:
        raise ValueError("Wrong input")


if __name__ == "__main__":
    database = "../Q_tunneling"
    #dirlist = ["20140526_chip5_tunneling", "20140526_chip6_tunneling",
    #           "chip8_raw_data_Q", "chip9"]

    #dirlist = ["20140526_chip5_tunneling", "20140526_chip6_tunneling"]
    #dirlist = ["chip8_raw_data_Q", "chip9"]
    dirlist = ["chip9", ]
    for dirname in dirlist:
        main(database, dirname)
