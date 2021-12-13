from typing import Dict, List
from lang import Lang
from pathlib import Path
from timeit import default_timer as timer
from concurrent.futures import ThreadPoolExecutor


class FindLang:
    langs: List[Lang]

    def __init__(self, references_path: str) -> None:
        self.langs = {}
        reference_paths = list(Path(references_path).rglob("*.utf8"))

        def func(reference_path): return Lang(str(reference_path), 5, 0.10)

        with ThreadPoolExecutor() as executor:
            langs = executor.map(func, reference_paths)
            self.langs = [l for l in langs]

    def find(self, target_path: str):
        def func(lang): return (lang.name, lang.estimate_bits(target_path))

        with ThreadPoolExecutor() as executor:
            results = executor.map(func, self.langs)

            return min(results, key=lambda r: r[1])[0]
