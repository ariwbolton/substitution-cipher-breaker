from typing import Generator
from collections import defaultdict


class BigramFrequencyMatrix:
    def __init__(self):
        self.m = defaultdict(int)
        self.ln_m = defaultdict(lambda x: float('-inf'))

    def read_words(self, word_generator: Generator[str, None, None]):
        for word in word_generator:
            self.read_word(word)


    def read_word(self, word: str):
        pass

    def generate_ln_m(self):
        pass
