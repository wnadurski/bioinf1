import sys

import global_seq
import handlers
import translation_RNA
from utils import get_input

debug = False


def print_ui():
    print "1 - wyznaczanie globalnego zestawienia (Needleman-Wunsh)"
    print "2 - wyznaczanie lokalnego zestawienia (Smith-Waterman)"
    print "x - Wyjscie"


# Mozna sobie dopisywac kolejne obslugi rzeczy z menu
command_map = {
    "x": sys.exit,
    "1": handlers.global_alignment,
    "2": handlers.local_alignment,
}


def do_nothing():
    pass


def handle_ui(command):
    if debug:
        print "Command: %s" % command
    command_map.get(command, do_nothing)()


if __name__ == "__main__":
    print_ui()

    try:
        while True:
            try:
                command = get_input()
            except EOFError:
                sys.exit()

            handle_ui(command)


            print ""
            print_ui()
    except KeyboardInterrupt:
        print ""
        sys.exit()
