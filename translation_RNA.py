from functools import partial

slownik = {'UUU': 'F', 'UUC': 'F', 'UUA': 'L', 'UUG': 'L', 'UCU': 'S', 'UCC': 'S', 'UCA': 'S', 'UCG': 'S', 'UAU': 'Y',
           'UAC': 'Y',
           'UAA': '!', 'UAG': '!', 'UGU': 'C', 'UGC': 'C', 'UGA': '!', 'UGG': 'W', 'CUU': 'L', 'CUC': 'L',
           'CUA': 'L', 'CUG': 'L',
           'CCU': 'P', 'CCC': 'P', 'CCA': 'P', 'CCG': 'P', 'CAU': 'H', 'CAC': 'H', 'CAA': 'Q', 'CAG': 'Q', 'CGU': 'R',
           'CGC': 'R',
           'CGA': 'R', 'CGG': 'R', 'AUU': 'I', 'AUC': 'I', 'AUA': 'I', 'AUG': 'M', 'ACU': 'T', 'ACC': 'T',
           'ACA': 'T', 'ACG': 'T',
           'AAU': 'N', 'AAC': 'N', 'AAA': 'K', 'AAG': 'K', 'AGU': 'S', 'AGC': 'S', 'AGA': 'R', 'AGG': 'R', 'GUU': 'V',
           'GUC': 'V',
           'GUA': 'V', 'GUG': 'V', 'GCU': 'A', 'GCC': 'A', 'GCA': 'A', 'GCG': 'A', 'GAU': 'D', 'GAC': 'D', 'GAA': 'E',
           'GAG': 'E',
           'GGU': 'G', 'GGC': 'G', 'GGA': 'G', 'GGG': 'G'
           }


def run_translation_DNA():
    przykladowasekwencja = "ACCGCCAGCCGCGACGAGA"


def rna_to_protein(seq):
    listseq = list(seq)
    proteins = []

    for x in range(0, len(listseq) - 3, 3):
        let = listseq[x]
        let1 = listseq[x + 1]
        let2 = listseq[x + 2]
        proteins.append(slownik[let + let1 + let2])

        print proteins

    return "".join(proteins)


def protein_to_RNA(seq):
    listseq = list(seq)
    allkodons=[]
    for x in range(len(listseq)):
        kodons = filter(partial(is_pair_witch_protein,listseq[x]),slownik.iteritems())[0]
        allkodons.append(kodons[0])
    return "".join(allkodons)
def is_pair_witch_protein(proteins,pair):
    return pair[1]==proteins