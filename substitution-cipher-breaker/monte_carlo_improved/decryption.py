from dataclasses import dataclass
from typing import Optional


@dataclass
class Decryption:
    key: 'SubstitutionKey'
    plaintext: str
    ln_score: Optional[float]
