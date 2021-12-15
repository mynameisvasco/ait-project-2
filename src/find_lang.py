from typing import List
from lang import Lang
from pathlib import Path
from concurrent.futures import ThreadPoolExecutor
from time import perf_counter


class FindLang:
    langs: List[Lang]

    def __init__(self, references_path: str) -> None:
        self.langs = []
        reference_paths = list(Path(references_path).rglob("*.utf8"))
        start = perf_counter()

        for reference_path in reference_paths:
            self.langs.append(Lang(str(reference_path), 5, 0.10))

        perf = (perf_counter() - start)
        print(f"Created all lang instances after {perf}s")

    def find(self, target_path: str):
        results = {}
        start = perf_counter()

        for lang in self.langs:
            results[lang.name] = lang.estimate_bits(target_path)

        perf = (perf_counter() - start) * 1000
        print(f"Found language of target after {perf}ms")
        return min(results.items(), key=lambda r: r[1])[0]
