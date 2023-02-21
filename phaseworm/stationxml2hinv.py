"""
PhaseNet wrapper to EarthWorm.

usage: phaseworm [-h] [-c CONFIG_FILE]

optional arguments:
  -h, --help            show this help message and exit
  -i, --input_stationxml STATIONXML_FILE
                        read inventory from STATIONXML_FILE file
  -o, --output_hinv HINV_FILE
                        write binder_ew inventory file into HINV_FILE file

:copyright:
    2020-2021   Jean-Marie Saurel <saurel@ipgp.fr>
                Lise Retailleau <retailleau@ipgp.fr>
                Claudio Satriano <satriano@ipgp.fr>

:license:
    GNU General Public License 3.0
    https://www.gnu.org/licenses/gpl-3.0.en.html
"""

import sys
import argparse
from obspy import read_inventory
from phaseworm.hinv_station_rw import print_hinv, write_hinv


# ___ INIT FUNCTIONS __________________________________________________________
def parse_args():
    """Parse command line arguments."""
    parser = argparse.ArgumentParser(description="Run StationXML to hinv converter")

    parser.add_argument("-o", "--output_hinv",
                        help="write output_hinv binder station file")
    parser.add_argument("-i", "--input_stationxml",
                        help="read inventory from input_stationxml file")
    args = parser.parse_args()

    return args


def unpack_list(string):
    """Unpack into a list a string containing comma-separated values."""
    # strip trailing commas, if any, then split
    outlist = string.rstrip(',').split(',')
    # strip extra whitespaces
    return [v.strip() for v in outlist]


# ___ END : INIT FUNCTIONS ____________________________________________________


# ___ MAIN LOOP _______________________________________________________________
def run_loop():
    """Parse arguments, read config and loop infinitely."""
    args = parse_args()

    if args.input_stationxml:
        stationxml = args.input_stationxml
        try:
            inv = read_inventory(stationxml)
        except Exception:
            print("Failed to load <%s> stationXML input file" % stationxml)
            exit()
    else:
        print("use -i option to select stationXML input file")
        exit()

    if args.output_hinv:
        n = write_hinv(inv, args.output_hinv)
        print("%d lines written in <%s> hinv file" % (n, args.output_hinv))
        exit()
    else:
        print("No output file given, print to standard output")
        print_hinv(inv)
    # Exit program
    exit()


def main():
    """Run the main loop and handle ctrl-C events."""
    try:
        run_loop()
    except KeyboardInterrupt:
        sys.stderr.write('\nAborting.\n')
        sys.exit()
# ___ END : MAIN LOOP _________________________________________________________


if __name__ == "__main__":
    main()
