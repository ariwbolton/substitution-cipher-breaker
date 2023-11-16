from collections import defaultdict
import math

from .ngram_parser import NGramParser
from .progress_context_manager import progress


class BigramFrequencyMatrix:
    def __init__(self):
        self.count = defaultdict(int)
        self.freq = defaultdict(int)

        # Can't default to -inf because we need to add probabilities
        # So, just use a very small number if the frequency is 0
        # "-10" roughly corresponds to assuming "0.01" occurrences in the corpus
        self.ln_freq = defaultdict(lambda: -10)

    @staticmethod
    def from_corpus(corpus_filename: str):
        with progress('Reading corpus'):
            with open(corpus_filename, 'r') as f:
                corpus = f.read()

        bfm = BigramFrequencyMatrix()
        bfm.read_text(corpus)

        return bfm

    def read_text(self, text: str):
        with progress('Counting bigrams'):
            for bigram in NGramParser.generate_bigrams(text):
                self.count[bigram] += 1

        with progress('Computing log freqs'):
            # Reset ln_freq
            self.ln_freq = defaultdict(lambda: -10)

            # Compute ln(f) for each bigram
            # ln(f) = ln(count[bigram] / total_bigrams)
            # ln(f) = ln(count[bigram]) - ln(total_bigrams)

            total_bigrams = sum(self.count.values())
            ln_total_bigrams = math.log(total_bigrams)

            for bigram in self.count:
                self.ln_freq[bigram] = math.log(self.count[bigram]) - ln_total_bigrams