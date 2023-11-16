## Markov Chain Monte Carlo

This algorithm implements a Markov Chain Monte Carlo algorithm to break substitution ciphers. In essence, it:

- Loads a representative set of bigram probabilities from a large corpus of English text
- Treats the space of all possible keys as a Markov chain, with bigram probabilities as transition probabilities
- Picks a starting key (fixed to be the unpermuted alphabet)
- Iteratively picks a random neighbor of the current key (by swapping two of the elements), and accepts it with a probability proportional to the likelihood of the resulting plaintext
  - Use log probabilities to avoid underflow
- After a large number of iterations, returns the most likely key (and resulting plaintext)

(This explanation was written long after the fact; the original code was written ~8 years beforehand. Python 2 is needed!
Some hardcoded environment variables, and some hard to understand constructs, are used.)