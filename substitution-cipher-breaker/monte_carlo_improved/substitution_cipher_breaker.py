import random
import math

from .bigram_frequency_matrix import BigramFrequencyMatrix
from .substitution_key import SubstitutionKey
from .decryption import Decryption
from .decryption_scorer import DecryptionScorer


class SubstitutionCipherBreaker:

    def __init__(self, *, bfm: BigramFrequencyMatrix):
        self.bfm = bfm
        self.scorer = DecryptionScorer(bfm=self.bfm)

    def break_code(self, ciphertext: str):
        k = SubstitutionKey.from_original_alphabet()
        d = self.get_scored_decryption(k, ciphertext)

        best_k = k
        best_d = d

        best_n_or_reset = 0

        reported_plaintexts = set()

        n = 0  # iteration number

        while n <= 1.5 * 10e3:
            if n % 1000 == 0:
                print(f'Iteration {n}, key: {k}, ln_score: {d.ln_score}')

            since_improvement = n - best_n_or_reset

            if since_improvement >= 3000 and since_improvement % 1000 == 0:
                # If we haven't made any progress, we should report the result, if we haven't already
                if d.plaintext not in reported_plaintexts:
                    print(d.plaintext)

                reported_plaintexts.add(d.plaintext)

                print('-> Resetting to random key')
                k = SubstitutionKey.random()
                d = self.get_scored_decryption(k, ciphertext)

                best_n_or_reset = n

            n += 1

            # Try up to N random swaps until we get one which is accepted, before starting over
            for i in range(4):
                k_prime = k.random_swapped()
                d_prime = self.get_scored_decryption(k_prime, ciphertext)

                # Non-deterministically accept or reject swap
                if SubstitutionCipherBreaker.accept(d=d, d_prime=d_prime):
                    k = k_prime
                    d = d_prime

                    if d.ln_score > best_d.ln_score:
                        best_k = k
                        best_d = d
                        best_n_or_reset = n

                    break

        print('\n=== Best ===')
        print(best_d.plaintext)

    def get_scored_decryption(self, k: SubstitutionKey, ciphertext: str):
        d = k.decryption(ciphertext)
        self.scorer.update_score(d)

        return d

    @staticmethod
    def accept(*, d: Decryption, d_prime: Decryption):
        """Always accept if d_prime is better. Otherwise, accept probabilistically."""
        if d_prime.ln_score > d.ln_score:
            return True

        # Use the ratio of (d' / d) as the probability of accepting d'
        # But, need to handle underflow; these are very small numbers (so we only have log values, anyways)
        # r = (d' / d)
        # ln(r) = ln(d') - ln(d)
        # r = e^(ln(d') - ln(d))

        r = math.exp(d_prime.ln_score - d.ln_score)
        p = random.random()

        return p < r



