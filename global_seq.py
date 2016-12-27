

match = 1
mismatch = -1
gap_penalty = -1

similarity_matrix = {
    'AA': match, 'AG': mismatch, 'AC': mismatch, 'AT': mismatch,
    'GA': mismatch, 'GG': match, 'GC': mismatch, 'GT': mismatch,
    'CA': mismatch, 'CG': mismatch, 'CC': match, 'CT': mismatch,
    'TA': mismatch, 'TG': mismatch, 'TC': mismatch, 'TT': match,
    }


def zeros_matrix(len1, len2):
    retval = []
    for x in range(len1):
        retval.append([])
        for y in range(len2):
            retval[-1].append(0)
    return retval


def init_score_matrix(rows, cols):
    matrix = zeros_matrix(rows, cols)
    for row in range(rows):
        matrix[row][0] = row * -1

    for col in range(cols):
        matrix[0][col] = col * -1

    return matrix


def run_traceback(a, i, j, seq1, seq2, s):
    aseq1 = ''
    aseq2 = ''

    while i > 0 and j > 0:


        # by preforming a traceback of how the matrix was filled out above,
        # i.e. we find a shortest path from a[n,m] to a[0,0]
        score = a[i][j]
        score_diag = a[i - 1][j - 1]
        score_up = a[i-1][j]
        score_left = a[i][j-1]

        if score == score_diag + s[seq1[i - 1] + seq2[j - 1]]:
            aseq1 = seq1[i - 1] + aseq1
            aseq2 = seq2[j - 1] + aseq2
            i -= 1
            j -= 1
        elif score == score_up + gap_penalty:
            aseq1 = seq1[i - 1] + aseq1
            aseq2 = '_' + aseq2
            i -= 1
        elif score == score_left + gap_penalty:
            aseq1 = '_' + aseq1
            aseq2 = seq2[j - 1] + aseq2
            j -= 1
        else:
            # should never get here..
            print 'ERROR'
            i = 0
            j = 0
            aseq1 = 'ERROR';
            aseq2 = 'ERROR';
            seq1 = 'ERROR';
            seq2 = 'ERROR'

    while i > 0:
        # If we hit j==0 before i==0 we keep going in i.
        aseq1 = seq1[i - 1] + aseq1
        aseq2 = '_' + aseq2
        i -= 1

    while j > 0:
        # If we hit i==0 before i==0 we keep going in j.
        aseq1 = '_' + aseq1
        aseq2 = seq2[j - 1] + aseq2
        j -= 1

    return aseq1, aseq2


def run_fill_phase(matrix, rows, cols, sim_matrix, seq1, seq2):
    for row in range(1, rows):
        for col in range(1, cols):
            score_left = matrix[row][col-1] + gap_penalty
            score_diagonal = matrix[row-1][col-1] + sim_matrix[(seq1[row - 1] + seq2[col - 1])]
            score_top = matrix[row-1][col] + gap_penalty
            matrix[row][col] = max(score_diagonal, score_left, score_top)

    return matrix


def run_global_sequence_algorithm(seq1, seq2, sim_matrix):
    print "Startujemy algorytm jazda"

    rows = len(seq1) + 1
    cols = len(seq2) + 1

    score_matrix = init_score_matrix(rows, cols)

    score_matrix = run_fill_phase(score_matrix, rows, cols, sim_matrix, seq1, seq2)
    print run_traceback(score_matrix, rows-1, cols-1, seq1, seq2, sim_matrix)

run_global_sequence_algorithm("GCATGCT", "GATTACA", similarity_matrix)


