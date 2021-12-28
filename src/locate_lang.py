from collections import defaultdict
from pathlib import Path
from typing import Dict, List, Tuple

from lang import Lang
from target import Target
from time import perf_counter


class LocateLang:
    lang_results: Dict[str, List[float]]
    lang_segments: Dict[str, List[Tuple[int, int]]]
    reference_chars: int
    threshold: int

    def __init__(self, references_path: str, target_path: str,
                 reference_chars: int, threshold: int) -> None:
        self.threshold = threshold
        self.lang_results = defaultdict(list)
        self.lang_segments = defaultdict(list)
        self.reference_chars = reference_chars
        reference_paths = list(Path(references_path).rglob("*.utf8"))
        langs = []

        print("Building references...")
        start = perf_counter()

        for reference_path in reference_paths:
            lang = Lang(str(reference_path), reference_chars)
            langs.append(lang)

        perf = (perf_counter() - start)
        print(f"Built all references after {perf}s")

        with open(target_path, "r") as target_file:
            target_text = target_file.read()
            target = Target(target_text, 5, None)

            for context, symbol in target.generator():
                for lang in langs:
                    bits = lang.estimate_bits(context, symbol)
                    self.lang_results[lang.name].append(bits)

    def find_lang_indexes(self):
        k = 5
        lang_name_list = list(self.lang_results)
        results_length = len(self.lang_results[lang_name_list[0]])
        best_count = 0
        current_best_lang = lang_name_list[0]
        segment_start = 0
        current_segment_fcm = ''

        for i in range(0, results_length):
            previous_best_fcm = current_best_lang
            current_best_lang = min(self.lang_results,
                                    key=lambda x: self.lang_results[x][i])

            # if an fcm is the best for the duration of the threshold then
            # start a new segment where that fcm is considered the best
            if current_best_lang == previous_best_fcm:
                best_count += 1
                if best_count == self.threshold and \
                        current_best_lang != current_segment_fcm:
                    if current_segment_fcm != '':
                        self.lang_segments[current_segment_fcm].append(
                            (segment_start, i - self.threshold))
                        segment_start = i - self.threshold
                    current_segment_fcm = current_best_lang
            else:
                best_count = 0

        self.lang_segments[current_best_lang].append(
            (segment_start, results_length + k - 1))
