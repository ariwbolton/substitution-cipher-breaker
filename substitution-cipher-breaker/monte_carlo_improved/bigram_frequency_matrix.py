import json
from collections import defaultdict
import math

from .ngram_parser import NGramParser
from .progress_context_manager import progress


class BigramFrequencyMatrix:
    def __init__(self):
        self.counts = defaultdict(int)

        # Can't default to -inf because we need to add probabilities
        # So, just use a very small number if the frequency is 0
        # "-10" roughly corresponds to assuming "0.01" occurrences in the corpus
        self.ln_freq = defaultdict(lambda: -10)

    # ------------------
    # Bigram Counts File
    # ------------------

    def counts_to_file(self, bigram_counts_filename: str):
        with progress('Writing bigram counts to file'):
            with open(bigram_counts_filename, 'w') as f:
                json.dump({f"{c1}|{c2}": count for (c1, c2), count in self.counts.items()}, f, indent=2)

    @staticmethod
    def from_counts_file(bigram_counts_filename: str):
        with progress('Reading bigram counts from file'):
            with open(bigram_counts_filename, 'r') as f:
                bigram_counts_serialized = json.load(f)

            bigram_counts_deserialized = {tuple(key.split('|')): count for key, count in bigram_counts_serialized.items()}
            counts = defaultdict(int, bigram_counts_deserialized)

            bfm = BigramFrequencyMatrix()
            bfm.update_counts(counts)

        return bfm

    def update_counts(self, counts):
        self.counts.update(counts)
        self.build_ln_freq()

    # ------
    # Corpus
    # ------

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
                self.counts[bigram] += 1

        self.build_ln_freq()

    # -------
    # Utility
    # -------

    def build_ln_freq(self):
        # Reset ln_freq
        self.ln_freq = defaultdict(lambda: -10)

        # Compute ln(f) for each bigram
        # ln(f) = ln(count[bigram] / total_bigrams)
        # ln(f) = ln(count[bigram]) - ln(total_bigrams)

        total_bigrams = sum(self.counts.values())
        ln_total_bigrams = math.log(total_bigrams)

        for bigram in self.counts:
            self.ln_freq[bigram] = math.log(self.counts[bigram]) - ln_total_bigrams
