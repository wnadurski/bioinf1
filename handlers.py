import re
from functools import partial

from global_seq import run_global_sequence_algorithm
from local_seq import run_local_sequence_algorithm
from utils import get_input


def get_inputs():
    return tuple(map(get_sequence, [
        "Podaj plik z pierwsza sekwencja:",
        "Podaj plik z druga sekwencja:",
        ("Podaj plik z macierza podobienstwa:", parse_matrix_file)
    ]))


def get_sequence(obj):
    if isinstance(obj, str):
        message, parser = obj, read_sequence
    else:
        message, parser = obj

    filename = get_input(message)
    try:
        with open(filename, "r") as f:
            return parser(f)
    except IOError:
        print "Nie udalo sie zaladowac pliku '%s'." % filename
        return get_sequence(obj)
    except Exception:
        print "Nie poprawny format pliku '%s'." % filename
        return get_sequence(obj)


def read_sequence(file):
    return re.sub("\s", "", file.read().strip())


def parse_matrix_file(f):
    line = f.readline()
    chars = line.split()
    matrix = []

    for row in range(len(chars)):
        line = f.readline()
        matrix.append([int(value) for value in line.split()])

    result = {}

    for row in range(len(chars)):
        for col in range(len(chars)):
            result[chars[row] + chars[col]] = matrix[row][col]

    return result


def alignment(algorithm):
    seq1, seq2, matrix = get_inputs()

    result = algorithm(seq1, seq2, matrix)

    print "Najlepsze dopasowanie:"
    print result
    print "\n"


global_alignment = partial(alignment, run_global_sequence_algorithm)
local_alignment = partial(alignment, run_local_sequence_algorithm)
