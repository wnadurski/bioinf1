import unittest

import handlers
import local_seq
import global_seq
import utils
from translation_RNA import rna_to_protein, protein_to_RNA


class LocalSeqTests(unittest.TestCase):
    def testVlabArmita(self):
        seq1 = "CGTGAATTCAT"
        seq2 = "GACTTAC"
        expected1 = "GAATT-C", "GACTTAC"
        sim_matrix = utils.make_similarity_matrix(5, -3)
        result = local_seq.run_local_sequence_algorithm(seq1, seq2, sim_matrix, -4)[0]
        self.assertEquals(expected1, result)

    def test_BinfSnipacademy(self):
        seq1 = "CGTTCTA"
        seq2 = "AACGTTGG"
        expected = "CGTT", "CGTT"
        sim_matrix = utils.make_similarity_matrix(5, -3)
        result = local_seq.run_local_sequence_algorithm(seq1, seq2, sim_matrix, -4)[0]
        self.assertEquals(expected, result)


class GlobalSeqTests(unittest.TestCase):
    def test_BinfSnipacademy(self):
        seq1 = "CGTTCTA"
        seq2 = "AACGTTGG"
        expected = "--CGTTCTA", "AACGTT-GG"
        sim_matrix = utils.make_similarity_matrix(5, -3)
        result = global_seq.run_global_sequence_algorithm(seq1, seq2, sim_matrix, -4)[0]
        self.assertEquals(expected, result)

    def test_short(self):
        seq1 = "ACGACG"
        seq2 = "ACGAT"
        expected = "ACGACG", "ACGA-T"
        sim_matrix = utils.make_similarity_matrix(1, -2)
        result = global_seq.run_global_sequence_algorithm(seq1, seq2, sim_matrix, -2)[0]
        self.assertEquals(expected, result)

    def distance_test(self):




class ParsingTests(unittest.TestCase):
    def test_matrix_parses_simple_matrix(self):
        filename = "inputs/matrix1.txt"

        expected = utils.make_similarity_matrix(1, -2)

        with open(filename, "r") as f:
            result = handlers.parse_matrix_file(f)

        self.assertEqual(expected, result)


class TranslationTests(unittest.TestCase):
    def test_RNA_translation(self):
        przykladowasekwencja = "ACCGCCAGCCGCGACGAGA"
        protein = rna_to_protein(przykladowasekwencja)
        self.assertEqual("TASRDE", protein)

    def test_protein_translation(self):
        przykladowasekwencja = "TASRDE"
        protein = protein_to_RNA(przykladowasekwencja)
        self.assertEqual("ACCGCGAGCCGGGAUGAA", protein)

@unittest.skip("Niepotrzebne")
class TestsWithBiopython(unittest.TestCase):
    def test_RNA_double_translation(self):
        from Bio.Seq import Seq

        from Bio.Alphabet import IUPAC
        seq = Seq("AUGGCCAUUGUAAUGGGCCGCUGAAAGGGUGCCCGAUAG", IUPAC.unambiguous_rna)

        print seq.translate().translate()

    def test_2(self):
        from Bio.SubsMat.MatrixInfo import blosum62
        print blosum62

        columns = []
        points = []

        for tup in blosum62.keys():
            if not tup[0] in columns:
                columns.append(tup[0])

        print columns

        for x, first in enumerate(columns):
            points.append([])
            for second in columns:
                try:
                    points[x].append(blosum62[(first,second)])
                except KeyError:
                    points[x].append(blosum62[(second, first)])


        for row in points:
            print row

        with open("inputs/blosum.txt", "w") as file:
            file.write("\t".join(columns))
            file.write("\n")

            for row in points:
                file.write("\t".join(map(str, row)))
                file.write("\n")



def main():
    unittest.main()


if __name__ == '__main__':
    main()
