## Improved Markov Chain Monte Carlo

This algorithm implements a Markov Chain Monte Carlo algorithm to break substitution ciphers. In essence, it:

- Loads a representative set of bigram probabilities from either a precomputed bigram table, or a large corpus of English text
- Treats the space of all possible keys as a Markov chain, with plaintext English likelihood as transition probabilities
- Picks a starting key
- Iteratively picks a random neighbor of the current key (by swapping two of the elements), and accepts it with a probability proportional to the likelihood of the resulting plaintext
  - Use log probabilities to avoid underflow
  - If the current key is likely a local maximum, pick a new random key, and continue
- After a fixed period of time, returns the best key (and resulting plaintext)

This algorithm builds on the algorithm in `historical/monte-carlo`.

- More or less a direct rewrite of the original code, but with (hopefully) clearer design
- Improved local maximum detection + handling
- Faster startup; relies on a precomputed bigram table
- More generic; allows more flexible configuration
- Improved termination handling (though not sophisticated; it's just a timeout)
- Migrates from Python 2 to 3, and uses modern language features

## Running

```bash
$ python3 -m substitution-cipher-breaker.monte_carlo_improved
```
