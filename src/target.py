
import re


class Target:
    text: str
    target_chars: int
    context_size: int

    def __init__(self, text: str, context_size: int, target_chars: int) -> None:
        self.text = ' '.join(i for i in text.split()
                             if i.isalpha() or i.isspace())

        if target_chars is not None and target_chars <= len(text):
            self.text = self.text[:target_chars]

        self.target_chars = target_chars
        self.context_size = context_size

    def generator(self):
        for i in range(len(self.text) - self.context_size):
            context = self.text[i:i + 5]
            symbol = self.text[i + self.context_size]
            yield (context, symbol)
