import random
import math

from bigram_frequency_matrix import BigramFrequencyMatrix
from corpus_parser import CorpusParser
from substitution_key import SubstitutionKey
from decryption import Decryption
from decryption_scorer import DecryptionScorer

class SubstitutionCipherBreaker:

    def __init__(self, *, corpus_filename: str):
        self.bfm = SubstitutionCipherBreaker.get_bigram_frequency_matrix(corpus_filename)
        self.scorer = DecryptionScorer(bfm=self.bfm)

    @staticmethod
    def get_bigram_frequency_matrix(corpus_filename: str) -> BigramFrequencyMatrix:
        cp = CorpusParser(corpus_filename)

        bfm = BigramFrequencyMatrix()

        bfm.read_words(cp.generate_words())
        bfm.generate_ln_m()

        return bfm

    def break_code(self, ciphertext: str):
        k = SubstitutionKey.from_original_alphabet()
        d = self.get_scored_decryption(k, ciphertext)

        n = 0  # iteration number

        while n < 5000:
            if n % 1000 == 0:
                print(f'Iteration {n}, key: {k}, ln_score: {d.ln_score}')
                print(d.plaintext)
                print('\n')

            n += 1

            k_prime = k.random_swapped()
            d_prime = self.get_scored_decryption(k, ciphertext)

            # Non-deterministically accept or reject swap
            if SubstitutionCipherBreaker.accept(d=d, d_prime=d_prime):
                k = k_prime
                d = d_prime

            # TODO: Figure out restart + termination conditions
            '''
            # Potential stopping point
            if n % 4000 == 0:
            	if f.lnPL < -2327:
            		# Restart algorithm if we're stuck in a local maxima
            		f = Perm()
            	else:
            		# Termination condition because
            		# we know what we're looking for
            		break
            '''

    def get_scored_decryption(self, k: SubstitutionKey, ciphertext: str):
        d = k.decryption(ciphertext)
        self.scorer.update_score(d)

        return d

    @staticmethod
    def accept(*, d: Decryption, d_prime: Decryption):
        """Always accept if d_prime is better. Otherwise, accept probabilistically."""
        if d_prime.ln_score > d.ln_score:
            return True

        r = math.exp(d_prime.ln_score - d.ln_score)
        p = random.random()

        return p < r



