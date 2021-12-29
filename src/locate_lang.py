from collections import defaultdict
from math import floor
from pathlib import Path
from typing import Dict, List, Tuple

from lang import Lang
from target import Target
from time import perf_counter


class LocateLang:
    lang_results: Dict[str, List[float]]
    lang_segments: List[Tuple[int, str]]
    reference_chars: int
    threshold: int

    def __init__(self, references_path: str, target_path: str,
                 reference_chars: int, smoothing_factor: int = 9) -> None:
        assert smoothing_factor % 2 != 0 and smoothing_factor > 0
        self.lang_results = defaultdict(list)
        self.lang_segments = []
        self.reference_chars = reference_chars
        self.smoothing_factor = smoothing_factor
        reference_paths = list(Path(references_path).rglob("*.utf8"))
        langs = []
        combination_threshold = 100
        lower_context_size = 3
        higher_context_size = 9
        self.higher_context_size = higher_context_size

        print(f"Building references...")
        start = perf_counter()

        for reference_path in reference_paths:
            low_depth_lang = Lang(str(reference_path), reference_chars, lower_context_size)
            high_depth_lang = Lang(str(reference_path), reference_chars, higher_context_size)
            langs.append(([low_depth_lang, [], 0], [high_depth_lang, [], 0]))

        perf = (perf_counter() - start)
        print(f"Built all references after {round(perf,3)}s")

        with open(target_path, "r") as target_file:
            text = target_file.read()

            target = Target(text, higher_context_size, None)

            for i, (context, symbol) in enumerate(target.generator(), start=1):
                for lang in langs:
                    low_depth_bits = lang[0][0].estimate_bits(context[-lower_context_size:], symbol)
                    lang[0][1].append(low_depth_bits)
                    high_depth_bits = lang[1][0].estimate_bits(context, symbol)
                    lang[1][1].append(high_depth_bits)
                    if low_depth_bits >= high_depth_bits:
                        lang[0][2] += 1
                    else:
                        lang[1][2] += 1
                    if i % combination_threshold == 0 or i == len(text) - higher_context_size: # could be wrong
                        low_depth_weight = lang[0][2] / (lang[0][2] + lang[1][2])
                        high_depth_weight = lang[1][2] / (lang[0][2] + lang[1][2])
                        for j in range(len(lang[0][1])):
                            weighted_value = low_depth_weight * lang[0][1][j] + high_depth_weight * lang[1][1][j]
                            self.lang_results[lang[0][0].name].append(weighted_value)
                        lang[0][1] = []
                        lang[1][1] = []
                        lang[0][2] = 0
                        lang[1][2] = 0

        self.smooth_complexity_profiles()

    def find_lang_indexes(self):
        lang_name_list = list(self.lang_results)
        results_length = len(self.lang_results[lang_name_list[0]])
        current_best_lang = lang_name_list[0]

        for i in range(0, results_length):
            previous_best_fcm = current_best_lang
            current_best_lang = min(self.lang_results,
                                    key=lambda x: self.lang_results[x][i])
            if current_best_lang != previous_best_fcm:
                if len(self.lang_segments) != 0:
                    self.lang_segments.append((i + self.higher_context_size, current_best_lang))
                else:
                    self.lang_segments.append((0, current_best_lang))

    def smooth_complexity_profiles(self):
        index_range = floor(self.smoothing_factor / 2)
        lang_names = list(self.lang_results)
        for i in range(len(self.lang_results[lang_names[0]])):
            for lang in lang_names:
                if i - index_range < 0:
                    lower_index = 0
                else:
                    lower_index = i - index_range
                if i + index_range > len(self.lang_results[lang]) - 1:
                    upper_index = len(self.lang_results[lang]) - 1
                else:
                    upper_index = i + index_range
                self.lang_results[lang][i] = sum(self.lang_results[lang][lower_index:upper_index+1]) / self.smoothing_factor
