import sys
from typing import Dict
from lang import Lang
from pathlib import Path
from time import perf_counter
from multiprocessing import Pool

PROCESSES_NUMBER = 5


class FindLang:
    langs: Dict[str, int]

    def __init__(self, references_path: str, target_path: str) -> None:
        self.langs = dict()
        reference_paths = list(Path(references_path).rglob("*.utf8"))
        start = perf_counter()
        pool = Pool(processes=PROCESSES_NUMBER)
        langs = []

        print(f"Building references...")

        for i, _ in enumerate(reference_paths):
            if i % PROCESSES_NUMBER == 0:
                langs = pool.map(
                    self.build_lang, reference_paths[i:i+PROCESSES_NUMBER])

                for lang in langs:
                    self.langs[lang.name] = lang.estimate_bits(target_path)

                langs.clear()

        perf = (perf_counter() - start)
        print(f"Builded all references after {perf}s")

    def build_lang(self, reference_path: Path):
        return Lang(str(reference_path))

    def find(self):
        return sorted(self.langs.items(), key=lambda r: r[1])
