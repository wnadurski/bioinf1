import utils


def init_score_matrix(rows, cols):
    matrix = utils.zeros_matrix(rows, cols)
    for row in range(rows):
        matrix[row][0] = row * -1

    for col in range(cols):
        matrix[0][col] = col * -1

    return matrix


def init_dist_matrix(rows, cols, gap_penalty=2):
    matrix = utils.zeros_matrix(rows, cols)
    for row in range(rows):
        matrix[row][0] = row * gap_penalty

    for col in range(cols):
        matrix[0][col] = col * gap_penalty
    return matrix


def run_traceback(a, traceback_matrix, seq1, seq2):
    aseq1, aseq2 = "", ""

    i, j = a

    while i > 0 or j > 0:

        if i > 0 and j > 0 and traceback_matrix[i][j] == 'diag':
            aseq1 = seq1[i - 1] + aseq1
            aseq2 = seq2[j - 1] + aseq2
            i -= 1
            j -= 1
        elif i > 0 or traceback_matrix[i][j] == 'top':
            aseq1 = seq1[i - 1] + aseq1
            aseq2 = '-' + aseq2
            i -= 1
        elif j > 0 or traceback_matrix[i][j] == 'left':
            aseq1 = '-' + aseq1
            aseq2 = seq2[j - 1] + aseq2
            j -= 1
        elif traceback_matrix[i][j] == 'end':
            return aseq1, aseq2

    return aseq1, aseq2


def run_fill_phase(score_matrix, traceback_matrix, distance_matrix, sim_matrix, seq1, seq2, gap_penalty):
    for x, row in enumerate(score_matrix):
        for y, value in enumerate(row):

            if x > 0 and y > 0:
                score_left = 'left', score_matrix[x][y - 1] + gap_penalty
                score_diagonal = 'diag', score_matrix[x - 1][y - 1] + sim_matrix[(seq1[x - 1] + seq2[y - 1])]
                score_top = 'top', score_matrix[x - 1][y] + gap_penalty

                distance_left = distance_matrix[x][y - 1] + gap_penalty
                distance_top = distance_matrix[x - 1][y] + gap_penalty
                distance_diagonal = distance_matrix[x - 1][y - 1] + sim_matrix[(seq1[x - 1] + seq2[y - 1])]

                min_distance = min(distance_left, distance_top, distance_diagonal)
                max_score = reduce(utils.compare_values, [score_left, score_diagonal, score_top])

                distance_matrix[x][y] = min_distance
                traceback_matrix[x][y], score_matrix[x][y] = max_score

    return traceback_matrix, distance_matrix


def add_gaps_to_matrix(matrix, gap_penalty):
    """

    :param matrix:
    :type matrix: dict
    :param gap_penalty:
    :return:
    """

    letters = map(lambda pair: pair[0], matrix.keys())
    for letter in letters:
        matrix["-" + letter] = gap_penalty
        matrix[letter + "-"] = gap_penalty


def calculate_similarity(alignment, similarity_matrix):
    seq1, seq2 = alignment

    score = 0

    for i, letter in enumerate(seq1):
        score += similarity_matrix[letter + seq2[i]]
    return score


def run_global_sequence_algorithm(seq1, seq2, sim_matrix=utils.similarity_matrix, gap_penalty=-2):
    rows = len(seq1) + 1
    cols = len(seq2) + 1

    add_gaps_to_matrix(sim_matrix, gap_penalty)

    traceback_matrix = utils.zeros_matrix(rows, cols)
    score_matrix = init_score_matrix(rows, cols)
    levenshtein_matrix = init_dist_matrix(rows, cols, gap_penalty)

    traceback_matrix, levenshtein_matrix = run_fill_phase(score_matrix, traceback_matrix, levenshtein_matrix,
                                                          sim_matrix, seq1, seq2, gap_penalty)

    distance = levenshtein_matrix[rows - 1][cols - 1]
    alignment = run_traceback((rows - 1, cols - 1), traceback_matrix, seq1, seq2)
    similarity_score = calculate_similarity(alignment, sim_matrix)
    return alignment, (distance, similarity_score)

# print run_global_sequence_algorithm("GCATGCT", "GATTACA", utils.similarity_matrix)
