import sys

import global_seq

debug = True


def print_ui():
    print "1 - wyznaczanie globalnej sekwencji (Needleman-Wunsh)"
    print "2 - wyznaczanie lokalnej sekwencji (Smith-Waterman)"
    print "3 - translacja RNA na aminokwasy"
    print "x - Wyjscie"


# Mozna sobie dopisywac kolejne obslugi rzeczy z menu
command_map = {
    "x": sys.exit,
    "1": global_seq.run_global_sequence_algorithm
}


def do_nothing():
    pass


def handle_ui(command):
    if debug:
        print "Command: %s" % command
    command_map.get(command, do_nothing)()


if __name__ == "__main__":
    print_ui()

    while True:
        try:
            command = raw_input("> ")
        except EOFError:
            sys.exit()
        handle_ui(command)

        print ""
        print_ui()
