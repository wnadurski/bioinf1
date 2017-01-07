from functools import reduce


def zeros_matrix(len1, len2):
    matrix = []
    for x in range(len1):
        matrix.append([])
        for y in range(len2):
            matrix[-1].append(0)
    return matrix


class MatrixCell:

    def __init__(self, value, index):
        self.value = value
        self.index = index
        self.descendant = ()

    def set_descendant_cell(self, index):
        self.descendant = index


def compare_values(a, b):
    if a[-1] >= b[-1]:
        return a
    return b


def matrix_max_index(matrix):
    matrix = [[(x, y, value) for y, value in enumerate(row)] for x, row in enumerate(matrix)]

    lst = map(lambda row: reduce(compare_values, row), matrix)

    return reduce(compare_values, lst)


def make_similarity_matrix(match=1, mismatch=-1):
    return {
    'AA': match, 'AG': mismatch, 'AC': mismatch, 'AT': mismatch,
    'GA': mismatch, 'GG': match, 'GC': mismatch, 'GT': mismatch,
    'CA': mismatch, 'CG': mismatch, 'CC': match, 'CT': mismatch,
    'TA': mismatch, 'TG': mismatch, 'TC': mismatch, 'TT': match,
    }

similarity_matrix = make_similarity_matrix()


def get_input(text=None):
    if not text is None:
        print text
    return raw_input("> ")