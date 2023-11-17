from .bigram_frequency_matrix import BigramFrequencyMatrix
from .ngram_parser import NGramParser


class BigramScorer:
    def __init__(self, *, bfm: BigramFrequencyMatrix):
        self.bfm = bfm

    def ln_score(self, text: str):
        """
        Get ln_score of the decryption. Optimized for speed.

        The score is the product of the probabilities of each bigram in the plaintext. But, this would cause underflow.
        So, we instead use the log probs and sum them.

        s = f1 * f2 * ... * fn
        ln(s) = ln(f1) + ln(f2) + ... + ln(fn)

        """
        return sum(self.bfm.ln_freq[bigram] for bigram in NGramParser.generate_bigrams(text))
