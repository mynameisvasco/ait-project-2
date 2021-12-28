from collections import defaultdict
from multiprocessing.pool import ThreadPool
from typing import Dict
from lang import Lang
from pathlib import Path
from time import perf_counter
from target import Target
import re
import string


class FindLang:
    target_chars: int
    references_chars: int
    estimations: Dict[str, int]

    def __init__(self, references_path: str, target_path: str, reference_chars: int, target_chars: int) -> None:
        self.estimations = defaultdict(int)
        self.references_chars = reference_chars
        self.target_chars = target_chars
        reference_paths = list(Path(references_path).rglob("*.utf8"))
        langs = []

        print(f"Building references...")
        start = perf_counter()

        for reference_path in reference_paths:
            lang = Lang(str(reference_path), reference_chars)
            langs.append(lang)

        perf = (perf_counter() - start)
        print(f"Built all references after {round(perf,3)}s")

        with open(target_path, "r") as target_file:
            text = ' '.join(i for i in "".join(target_file.readlines()[:500]).split()
                            if not i.isnumeric())
            text = re.sub(rf"[{string.punctuation}]", "", text)

            if target_chars is not None and target_chars <= len(text):
                text = text[:target_chars]

            target = Target(text, 5, self.target_chars)

            for context, symbol in target.generator():
                for lang in langs:
                    bits = lang.estimate_bits(context, symbol)
                    self.estimations[lang.name] += bits

    def find(self):
        return sorted(self.estimations.items(), key=lambda r: r[1])[0]
