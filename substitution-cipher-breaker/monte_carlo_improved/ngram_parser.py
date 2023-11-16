from typing import Generator, Tuple


class NGramParser:

    @staticmethod
    def generate_bigrams(s: str) -> Generator[Tuple[str, str], None, None]:
        """Generate bigrams for a string. Optimized for speed."""
        len_s_1 = len(s) - 1

        if len(s) == 0:
            return

        if s[0].isalpha():
            yield ' ', s[0]

        if len(s) > 1:
            for i in range(len(s) - 1):
                # normalize non-alphabetic characters to spaces
                c1 = s[i]     if s[i].isalpha()     else ' '
                c2 = s[i + 1] if s[i + 1].isalpha() else ' '

                if c1.isalpha() or c2.isalpha():  # skip whitespace-only bigrams
                    yield c1, c2

        if s[-1].isalpha():
            yield s[-1], ' '
