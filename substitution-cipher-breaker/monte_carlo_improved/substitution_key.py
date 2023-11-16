import copy
import random
from typing import Dict
import string

from .decryption import Decryption


class SubstitutionKey:
    def __init__(self, *, mapping: Dict[str, str]):
        self.mapping = copy.copy(mapping)

    @staticmethod
    def from_key(key: 'SubstitutionKey'):
        return SubstitutionKey(mapping=key.mapping)

    @staticmethod
    def from_original_alphabet():
        return SubstitutionKey(mapping={c: c for c in string.ascii_lowercase})

    @staticmethod
    def random():
        shuffled = list(string.ascii_lowercase)

        random.shuffle(shuffled)

        return SubstitutionKey(mapping={c: r for c, r in zip(list(string.ascii_lowercase), shuffled)})

    def swapped(self, i: str, j: str):
        new_mapping = self.mapping.copy()
        new_mapping[i], new_mapping[j] = new_mapping[j], new_mapping[i]

        return SubstitutionKey(mapping=new_mapping)

    def random_swapped(self):
        i, j = random.sample(string.ascii_lowercase, 2)

        return self.swapped(i, j)

    def decryption(self, ciphertext: str) -> Decryption:
        plaintext = "".join(self.mapping[c] if c.isalpha() else c for c in ciphertext)

        return Decryption(key=self, plaintext=plaintext, ln_score=None)

    def __repr__(self):
        return ''.join(self.mapping[c] for c in string.ascii_lowercase)
