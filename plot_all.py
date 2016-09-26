# scripts that runs all the plotting
import os
import glob
from fit_gate_chip import fit_one_file


def plot1(database, dirname):
    print(os.path.join(database, dirname, "*"))
    subdirs = glob.glob(os.path.join(database, dirname, "*"))
    print("subdirs: %s" % subdirs)
    subdirs.sort()
    for subdir1 in subdirs:
        filelist = glob.glob(os.path.join(subdir1, "*.dat"))
        filelist.sort()
        for datafile in filelist:
            # plot only(no save)
            #fit_one_file(datafile)
            # save plot only
            fit_one_file(datafile, outputdir=subdir1)


def plot2(database, dirname):
    subdirs = glob.glob(os.path.join(database, dirname, "*"))
    subdirs.sort()
    for subdir1 in subdirs:
        subdirs1 = glob.glob(os.path.join(subdir1, "*"))
        for subdir2 in subdirs1:
            filelist = glob.glob(os.path.join(subdir2, "*.dat"))
            filelist.sort()
            for datafile in filelist:
                # plot only(no save)
                #fit_one_file(datafile)
                # save plot only
                fit_one_file(datafile, outputdir=subdir2)


def main(database, dirname):

    if dirname in ["20140526_chip5_tunneling", "20140526_chip6_tunneling"]:
        plot1(database, dirname)
    elif dirname in ["chip9", "chip8_raw_data_Q"]:
        plot2(database, dirname)
    else:
        raise ValueError("Wrong input")


if __name__ == "__main__":
    database = "../Q_tunneling"
    dirlist = ["20140526_chip5_tunneling", "20140526_chip6_tunneling",
               "chip8_raw_data_Q", "chip9"]

    #dirlist = ["chip8_raw_data_Q", ]
    for dirname in dirlist:
        main(database, dirname)
