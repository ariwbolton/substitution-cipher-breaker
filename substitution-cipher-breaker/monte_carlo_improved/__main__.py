from . import SubstitutionCipherBreaker
from ..data import ciphertexts

breaker = SubstitutionCipherBreaker(corpus_filename='./substitution-cipher-breaker/data/war-and-peace.txt')

breaker.break_code(ciphertext=ciphertexts.c1)

