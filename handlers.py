import re
from functools import partial

from global_seq import run_global_sequence_algorithm
from local_seq import run_local_sequence_algorithm
from translation_RNA import rna_to_protein, protein_to_RNA
from utils import get_input, get_command

DNA_ALIGNMENT = "1"
RNA_ALIGNMENT = "2"

def get_inputs():
    print "1 - Zestawienie sekwencji DNA"
    print "2 - Zestawienie sekwencji kodonow (mRNA jako sekwencje wejsciowe)"

    command = get_command(["1", "2"])

    return tuple([command] + map(get_sequence, [
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
    seq_type, seq1, seq2, matrix = get_inputs()

    if (seq_type == RNA_ALIGNMENT):
        seq1, seq2 = rna_to_protein(seq1), rna_to_protein(seq2)

    result = algorithm(seq1, seq2, matrix)

    align1 = result[0][0]
    align2 = result[0][1]

    if (seq_type == RNA_ALIGNMENT):
        align1, align2 = protein_to_RNA(align1), protein_to_RNA(align2)

    print "Najlepsze dopasowanie:"
    print align1
    print align2
    print "Odleglosc edycyjna: %d. Podobienstwo: %f" % (result[1][0], result[1][1])
    print "\n"


global_alignment = partial(alignment, run_global_sequence_algorithm)
local_alignment = partial(alignment, run_local_sequence_algorithm)
