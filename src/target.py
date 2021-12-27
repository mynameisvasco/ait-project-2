from typing import ContextManager


from time import perf_counter


class Target:
    text: str
    context_size: int

    def __init__(self, text: str, context_size: int) -> None:
        self.text = text
        self.context_size = context_size

    def generator(self):
        for i in range(len(self.text) - self.context_size):
            context = self.text[i:i + 5]
            symbol = self.text[i + self.context_size]
            yield (context, symbol)
