from collections import defaultdict
from multiprocessing.pool import ThreadPool
from typing import Dict
from lang import Lang
from pathlib import Path
from time import perf_counter

from target import Target


class FindLang:
    langs: Dict[str, int]

    def __init__(self, references_path: str, target_path: str) -> None:
        self.langs = defaultdict(int)
        reference_paths = list(Path(references_path).rglob("*.utf8"))
        pool = ThreadPool()
        langs = []

        print(f"Building references...")
        start = perf_counter()
        langs = pool.map(lambda rp: Lang(str(rp)), reference_paths)
        perf = (perf_counter() - start)
        print(f"Builded all references after {perf}s")

        with open(target_path, "r") as target_file:
            target = Target(target_file.read(), 5)

            for i, (context, symbol) in enumerate(target.generator()):
                for lang in langs:
                    self.langs[lang.name] += lang.estimate_bits(
                        context, symbol)
                if i % 1000 == 0:
                    print(i)

    def find(self):
        return sorted(self.langs.items(), key=lambda r: r[1])
