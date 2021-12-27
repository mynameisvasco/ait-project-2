from collections import defaultdict
from typing import Dict, List, Tuple

from fcm import Fcm


class LocateLang:
    fcms: Tuple[Fcm, ...]
    fcms_results: Dict[str, List[float]]
    # fcm_indexes: Dict[str, List[int]]
    fcm_indexes: Dict[str, List[Tuple[int, int]]]
    threshold: int

    # TODO: instead of receiving the Fcm instances receive the paths and cache
    # if necessary
    def __init__(self, threshold, *fcms: Fcm) -> None:
        self.threshold = threshold
        self.fcms = fcms
        self.fcms_results = defaultdict(list)
        self.fcm_indexes = defaultdict(list)

    def generate_fcm_results(self, target_path: str):
        context_sizes = [fcm.context_size for fcm in self.fcms]
        max_context_size = max(context_sizes)

        with open(target_path) as target_file:
            target_text = target_file.read()

            for i in range(max_context_size, len(target_text)):
                context = target_text[i - max_context_size:i]
                for j, fcm in enumerate(self.fcms, start=1):
                    # TODO: this needs to change according to the
                    # reference file's name
                    fcm_name = f'fcm{j}'
                    self.fcms_results[fcm_name].append(
                        fcm.get_information_amount(
                            target_text[i], context[-fcm.context_size:]))

    def find_fcm_indexes(self):
        k = 3
        fcm_name_list = list(self.fcms_results.keys())
        nr_chars = len(self.fcms_results['fcm1'])
        best_count = 0
        current_best_fcm = fcm_name_list[0]

        segment_start = 0
        current_segment_fcm = ''
        for i in range(0, nr_chars):
            previous_best_fcm = current_best_fcm
            current_best_fcm = min(self.fcms_results,
                                   key=lambda x: self.fcms_results[x][i])

            # if an fcm is the best for the duration of the threshold then
            # start a new segment where that fcm is considered the best
            if current_best_fcm == previous_best_fcm:
                best_count += 1
                if best_count == self.threshold and \
                        current_best_fcm != current_segment_fcm:
                    if current_segment_fcm != '':
                        self.fcm_indexes[current_segment_fcm].append(
                            (segment_start, i - self.threshold))
                        segment_start = i - self.threshold
                    current_segment_fcm = current_best_fcm
            else:
                best_count = 0

        self.fcm_indexes[current_best_fcm].append(
            (segment_start, nr_chars + k - 1))
