import unittest

import handlers
import local_seq
import global_seq
import utils

class LocalSeqTests(unittest.TestCase):

    def testVlabArmita(self):
        seq1 = "CGTGAATTCAT"
        seq2 = "GACTTAC"
        expected1 = "GAATT-C", "GACTTAC"
        sim_matrix = utils.make_similarity_matrix(5, -3)
        result = local_seq.run_local_sequence_algorithm(seq1, seq2, sim_matrix, -4)
        self.assertEquals(expected1, result)

    def testFoo(self):
        seq1 = "TACGGGCCCGCTAC"
        seq2 = "TAGCCCTATCGGTCA"
        expected = "TACGGGCCCGCTA-C", "TA---G-CC-CTATC"
        result = local_seq.run_local_sequence_algorithm(seq1, seq2, utils.similarity_matrix)
        self.assertEquals(expected, result)

    def test_BinfSnipacademy(self):
        seq1 = "CGTTCTA"
        seq2 = "AACGTTGG"
        expected = "CGTT", "CGTT"
        sim_matrix = utils.make_similarity_matrix(5, -3)
        result = local_seq.run_local_sequence_algorithm(seq1, seq2, sim_matrix, -4)
        self.assertEquals(expected, result)


class GlobalSeqTests(unittest.TestCase):
    def test_chuj(self):
        seq1 = "AATTATGCTTAATG"
        seq2 = "AGTCAATTTTAACTGA"
        expected = "----AATTATGCTTAA-TG-", "AGTCAATT----TTAACTGA"
        result = global_seq.run_global_sequence_algorithm(seq1, seq2)
        self.assertEquals(expected, result)

    def test_BinfSnipacademy(self):
        seq1 = "CGTTCTA"
        seq2 = "AACGTTGG"
        expected = "--CGTTCTA", "AACGTT-GG"
        sim_matrix = utils.make_similarity_matrix(5, -3)
        result = global_seq.run_global_sequence_algorithm(seq1, seq2, sim_matrix, -4)
        self.assertEquals(expected, result)

class ParsingTests(unittest.TestCase):
    def test_matrix_parses_simple_matrix(self):
        filename = "inputs/matrix1.txt"

        expected = utils.make_similarity_matrix(1, -2)

        with open(filename, "r") as f:
            result = handlers.parse_matrix_file(f)

        self.assertEqual(expected, result)


def main():
    unittest.main()

if __name__ == '__main__':
    main()