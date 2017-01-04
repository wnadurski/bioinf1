import utils


def init_score_matrix(rows, cols):
    matrix = utils.zeros_matrix(rows, cols)
    for row in range(rows):
        matrix[row][0] = row * -1

    for col in range(cols):
        matrix[0][col] = col * -1

    return matrix


def run_traceback(a, dupa, seq1, seq2):
    aseq1, aseq2 = "", ""

    i, j = a

    while i > 0 or j > 0:

        if i > 0 and j > 0 and dupa[i][j] == 'diag':
            aseq1 = seq1[i - 1] + aseq1
            aseq2 = seq2[j - 1] + aseq2
            i -= 1
            j -= 1
        elif i > 0 or dupa[i][j] == 'top':
            aseq1 = seq1[i - 1] + aseq1
            aseq2 = '-' + aseq2
            i -= 1
        elif j > 0 or dupa[i][j] == 'left':
            aseq1 = '-' + aseq1
            aseq2 = seq2[j - 1] + aseq2
            j -= 1
        elif dupa[i][j] == 'end':
            return aseq1, aseq2

    return aseq1, aseq2


def run_fill_phase(score_matrix, traceback_matrix, sim_matrix, seq1, seq2, gap_penalty):

    for x, row in enumerate(score_matrix):
        for y, value in enumerate(row):

            if x > 0 and y > 0:

                score_left = 'left', score_matrix[x][y - 1] + gap_penalty
                score_diagonal = 'diag', score_matrix[x - 1][y - 1] + sim_matrix[(seq1[x - 1] + seq2[y - 1])]
                score_top = 'top', score_matrix[x - 1][y] + gap_penalty

                max_score = reduce(utils.compare_values, [score_left, score_diagonal, score_top])
                traceback_matrix[x][y], score_matrix[x][y] = max_score

    return traceback_matrix


def run_global_sequence_algorithm(seq1, seq2, sim_matrix=utils.similarity_matrix, gap_penalty=0):

    rows = len(seq1) + 1
    cols = len(seq2) + 1

    traceback_matrix = utils.zeros_matrix(rows, cols)
    score_matrix = init_score_matrix(rows, cols)

    traceback_matrix = run_fill_phase(score_matrix, traceback_matrix, sim_matrix, seq1, seq2, gap_penalty)

    return run_traceback((rows-1, cols-1), traceback_matrix, seq1, seq2)

run_global_sequence_algorithm("GCATGCT", "GATTACA", utils.similarity_matrix)


