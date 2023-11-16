from bigram_frequency_matrix import BigramFrequencyMatrix
from decryption import Decryption


class DecryptionScorer:
    def __init__(self, *, bfm: BigramFrequencyMatrix):
        self.bfm = bfm

    def update_score(self, d: Decryption):
        """Set the ln_score of the decryption. Optimized for speed."""
        pt = d.plaintext
        ln_score = 0
        bfm = self.bfm

        # Set score on decryption
        for i in range(-1, len(pt)):
            # include beginning and end bigrams, and normalize non-alphabetic characters to spaces
            c1 = pt[i]     if i >= 0          and pt[i].isalpha()     else ' '
            c2 = pt[i + 1] if i < len(pt) - 1 and pt[i + 1].isalpha() else ' '

            if c1.isalpha() or c2.isalpha():  # only consider bigrams with at least one alphabetic character
                ln_score += bfm.ln_m[(c1, c2)]

        # TODO: Figure out this piece!!
        # Number of bigrams is 458 in ciphertext
        # ln_score -= 458 * self.lnS

        d.ln_score = ln_score
