## Brute Force + Dictionary

The simplest method looks roughly as follows:

- Load a dictionary of english words (not supplied)
- Start filling out portions of the key for the first word in the ciphertext
- Iteratively use that partial key to help decrypt each additional word of the ciphertext
- If the current word cannot be decrypted into a valid word using the current key + dictionary, assume the current key is invalid, and backtrack

One poor heuristic used is to sort the words in the ciphertext by length and operate on words in order.

(This explanation was written long after the fact; the original code was written ~8 years beforehand. Python 2 is needed!
Why was the file named `reverse_decrypt.py`? I have no idea.)