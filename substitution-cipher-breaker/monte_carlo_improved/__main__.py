from . import SubstitutionCipherBreaker
from .bigram_frequency_matrix import BigramFrequencyMatrix
from ..data import ciphertexts

bfm = BigramFrequencyMatrix.from_counts_file('./substitution-cipher-breaker/data/bigram_counts.json')
breaker = SubstitutionCipherBreaker(bfm=bfm)

breaker.break_code(ciphertext=ciphertexts.c1)
