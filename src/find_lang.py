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
        combination_threshold = 100
        lower_context_size = 3
        higher_context_size = 9

        print(f"Building references...")
        start = perf_counter()

        for reference_path in reference_paths:
            low_depth_lang = Lang(str(reference_path),
                                  reference_chars, lower_context_size)
            high_depth_lang = Lang(str(reference_path),
                                   reference_chars, higher_context_size)
            langs.append(([low_depth_lang, [], 0], [high_depth_lang, [], 0]))

        perf = (perf_counter() - start)
        print(f"Built all references after {round(perf,3)}s")

        with open(target_path, "r") as target_file:
            text = ' '.join(i for i in "".join(target_file.readlines()[:500]).split()
                            if not i.isnumeric())
            text = re.sub(rf"[{string.punctuation}]", "", text)

            if target_chars is not None and target_chars <= len(text):
                text = text[:target_chars]

            target = Target(text, higher_context_size, self.target_chars)

            for i, (context, symbol) in enumerate(target.generator(), start=1):
                for lang in langs:
                    low_depth_bits = lang[0][0].estimate_bits(
                        context[-lower_context_size:], symbol)
                    lang[0][1].append(low_depth_bits)
                    high_depth_bits = lang[1][0].estimate_bits(context, symbol)
                    lang[1][1].append(high_depth_bits)
                    if low_depth_bits >= high_depth_bits:
                        lang[0][2] += 1
                    else:
                        lang[1][2] += 1
                    if i % combination_threshold == 0 or i == self.target_chars:
                        low_depth_weight = lang[0][2] / \
                            (lang[0][2] + lang[1][2])
                        low_depth_sum = sum(lang[0][1])
                        high_depth_weight = lang[1][2] / \
                            (lang[0][2] + lang[1][2])
                        high_depth_sum = sum(lang[1][1])
                        self.estimations[lang[0][0].name] += low_depth_weight * \
                            low_depth_sum + high_depth_weight * high_depth_sum
                        lang[0][1] = []
                        lang[1][1] = []
                        lang[0][2] = 0
                        lang[1][2] = 0

    def find(self):
        return sorted(self.estimations.items(), key=lambda r: r[1])[0]
