from .bigram_frequency_matrix import BigramFrequencyMatrix
from .substitution_key import SubstitutionKey
from .bigram_scorer import BigramScorer
from .markov_chain_visitor import MarkovChainVisitor
from .markov_chain import MarkovChain


class SubstitutionCipherBreaker:

    def __init__(self, *, bfm: BigramFrequencyMatrix):
        self.bfm = bfm

    def break_code(self, ciphertext: str):
        visitor = MarkovChainVisitor(
            markov_chain=MarkovChain(
                scorer=BigramScorer(bfm=self.bfm),
                ciphertext=ciphertext
            ),
            k=SubstitutionKey.from_original_alphabet(),
            timeout_s=15
        )

        should_step = True

        try:
            while should_step:
                should_step = visitor.step()
        except KeyboardInterrupt:
            print('KeyboardInterrupt - Exiting...')

        print('\n=== Best ===')
        print(visitor.best.d.plaintext)



