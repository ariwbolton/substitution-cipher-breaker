from typing import Generator


class CorpusParser:
    def __init__(self, filename):
        self.filename = filename

    def generate_words(self) -> Generator[str, None, None]:
        with open(self.filename, 'r') as f:
            lines = f.readlines()

        # TODO
        return lines