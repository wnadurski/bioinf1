import utils
from global_seq import calculate_similarity, add_gaps_to_matrix


def init_score_matrix(rows, cols):
    matrix = utils.zeros_matrix(rows, cols)
    for row in range(rows):
        matrix[row][0] = 0

    for col in range(cols):
        matrix[0][col] = 0

    return matrix


def run_traceback(a, traceback_matrix, seq1, seq2):
    aseq1, aseq2 = "", ""

    i, j, dummy = a

    while i > 0 or j > 0:

        if i > 0 and j > 0 and traceback_matrix[i][j] == 'diag':
            aseq1 = seq1[i - 1] + aseq1
            aseq2 = seq2[j - 1] + aseq2
            i -= 1
            j -= 1
        elif i > 0 and traceback_matrix[i][j] == 'top':
            aseq1 = seq1[i - 1] + aseq1
            aseq2 = '-' + aseq2
            i -= 1
        elif j > 0 and traceback_matrix[i][j] == 'left':
            aseq1 = '-' + aseq1
            aseq2 = seq2[j - 1] + aseq2
            j -= 1
        elif traceback_matrix[i][j] == 'end' or traceback_matrix[i][j] == 0:
            return aseq1, aseq2

    return aseq1, aseq2


def run_fill_phase(score_matrix, traceback_matrix, distance_matrix, sim_matrix, seq1, seq2, gap_penalty):

    for x, row in enumerate(score_matrix):
        for y, value in enumerate(row):

            if x > 0 and y > 0:

                score_left = 'left', score_matrix[x][y - 1] + gap_penalty
                score_diagonal = 'diag', score_matrix[x - 1][y - 1] + sim_matrix[(seq1[x - 1] + seq2[y - 1])]
                score_top = 'top', score_matrix[x - 1][y] + gap_penalty
                score_zero = 'end', 0

                distance_left = score_matrix[x][y - 1] + 1
                distance_top = score_matrix[x - 1][y] + 1
                distance_diagonal = score_matrix[x - 1][y - 1] + (0 if seq1[x - 1] == seq2[y - 1] else 1)

                min_distance = min(distance_left, distance_top, distance_diagonal)
                max_score = reduce(utils.compare_values, [score_zero, score_left, score_diagonal, score_top])

                distance_matrix[x][y] = min_distance
                traceback_matrix[x][y], score_matrix[x][y] = max_score

    return traceback_matrix


def run_local_sequence_algorithm(seq1, seq2, sim_matrix, gap_penalty=-2):

    rows = len(seq1) + 1
    cols = len(seq2) + 1

    add_gaps_to_matrix(sim_matrix, gap_penalty)

    score_matrix = init_score_matrix(rows, cols)
    traceback_matrix = init_score_matrix(rows, cols)
    levenshtein_matrix = utils.zeros_matrix(rows, cols)

    traceback_matrix = run_fill_phase(score_matrix, traceback_matrix, levenshtein_matrix, sim_matrix, seq1, seq2, gap_penalty)
    max_index = utils.matrix_max_index(score_matrix)
    result = run_traceback(max_index, traceback_matrix, seq1, seq2)
    distance = levenshtein_matrix[rows - 1][cols - 1]
    similarity_score = calculate_similarity(result, sim_matrix)

    return result, (distance, similarity_score)

run_local_sequence_algorithm("AGG", "ATG", utils.similarity_matrix, 0)