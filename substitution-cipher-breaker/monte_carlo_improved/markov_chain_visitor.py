import math
import random
import time

from .substitution_key import SubstitutionKey
from .markov_chain import MarkovChain, MarkovChainNode


class MarkovChainVisitor:
    def __init__(self, *, k: SubstitutionKey, markov_chain: MarkovChain, timeout_s: int = 15):
        """
        :param k: Initial key
        :param markov_chain: Markov chain to traverse
        :param timeout_s: Timeout in seconds
        """
        self.markov_chain = markov_chain

        self.round = 0

        self.current = self.markov_chain.node(k)

        self.last_accepted = self.current
        self.best = self.current
        self.best_or_reset_round = 0
        self.reported_plaintexts = set()

        self.batch_rounds = 1000
        self.no_recent_improvement_batches = 3

        self.start_time = time.time()
        self.timeout_s = timeout_s

    def step(self) -> bool:
        """Step through the chain. Return False if we should stop."""
        self.round += 1

        if self.is_batch_end():
            self.log_round()

            if self.is_timeout():
                return False

            if self.no_recent_improvement():
                self.report_plaintext_idempotently()

                print('-> Resetting to random key')
                self.best_or_reset_round = self.round
                self.set_current(self.markov_chain.get_random_node())

                return True

        _next = self.markov_chain.get_random_neighbor(self.current)

        if self.accept(_next):
            self.set_current(_next)

        return True

    # =========
    # Traversal
    # =========

    def set_current(self, node: MarkovChainNode):
        self.current = node
        self.last_accepted = node

        self.update_best()

    def update_best(self):
        if self.current.d.ln_score > self.best.d.ln_score:
            self.best = self.current
            self.best_or_reset_round = self.round

    def accept(self, node: MarkovChainNode):
        """Always accept if d' is better. Otherwise, accept probabilistically."""
        if node.d.ln_score > self.current.d.ln_score:
            return True

        # Use the ratio of (d' / d) as the probability of accepting d'
        # But, need to handle underflow; these are very small numbers (so we only have log values, anyways)
        # r = (d' / d)
        # ln(r) = ln(d') - ln(d)
        # r = e^(ln(d') - ln(d))

        r = math.exp(node.d.ln_score - self.current.d.ln_score)
        p = random.random()

        return p < r

    # =========
    # Resetting
    # =========

    def no_recent_improvement(self):
        lookback_rounds = (self.batch_rounds * self.no_recent_improvement_batches)

        return self.round - self.best_or_reset_round > lookback_rounds

    # =======
    # Logging
    # =======

    def is_batch_end(self):
        return self.round % self.batch_rounds == 0

    def log_round(self):
        print(f'{self.round}, key: {self.current.k}, ln_score: {self.current.d.ln_score}')

    def is_timeout(self):
        return time.time() - self.start_time > self.timeout_s

    def report_plaintext_idempotently(self):
        if self.current.d.plaintext not in self.reported_plaintexts:
            self.reported_plaintexts.add(self.current.d.plaintext)
            print(self.current.d.plaintext)


