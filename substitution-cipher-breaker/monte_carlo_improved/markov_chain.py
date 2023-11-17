from dataclasses import dataclass

from .bigram_scorer import BigramScorer
from .substitution_key import SubstitutionKey


@dataclass
class MarkovChainNode:
    k: 'SubstitutionKey'
    d: 'Decryption'


class MarkovChain:
    def __init__(self, *, ciphertext: str, scorer: BigramScorer):
        self.ciphertext = ciphertext
        self.scorer = scorer

    def node(self, k: SubstitutionKey):
        d = k.decryption(self.ciphertext)
        d.ln_score = self.scorer.ln_score(d.plaintext)

        return MarkovChainNode(k=k, d=d)

    def get_random_neighbor(self, node: MarkovChainNode):
        return self.node(node.k.random_swapped())

    def get_random_node(self):
        return self.node(SubstitutionKey.random())
