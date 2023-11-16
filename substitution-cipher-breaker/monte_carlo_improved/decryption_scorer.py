from .bigram_frequency_matrix import BigramFrequencyMatrix
from .decryption import Decryption
from .ngram_parser import NGramParser


class DecryptionScorer:
    def __init__(self, *, bfm: BigramFrequencyMatrix):
        self.bfm = bfm

    def update_score(self, d: Decryption):
        """
        Set the ln_score of the decryption. Optimized for speed.

        The score is the product of the probabilities of each bigram in the plaintext. But, this would cause underflow.
        So, we instead use the log probs and sum them.

        s = f1 * f2 * ... * fn
        ln(s) = ln(f1) + ln(f2) + ... + ln(fn)

        """
        ln_score = 0
        bfm = self.bfm

        for bigram in NGramParser.generate_bigrams(d.plaintext):
            ln_score += bfm.ln_freq[bigram]

        # TODO: Figure out this piece!!
        # Number of bigrams is 458 in ciphertext
        # ln_score -= 458 * self.lnS

        d.ln_score = ln_score
