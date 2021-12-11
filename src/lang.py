from math import ceil
from fcm import Fcm
from pathlib import Path
import pickle


class Lang:
    reference: Fcm

    def __init__(self, reference_path: str, context_size: int, smoothing: float) -> None:
        reference_path_base = reference_path.split('/')[-1]
        cache_path = Path(
            f"cache/{reference_path_base}_{context_size}_{smoothing}.cache")

        if cache_path.exists():
            with open(cache_path, "rb") as cache_file:
                self.reference = pickle.load(cache_file)
        else:
            self.reference = Fcm(smoothing, context_size)

            with open(reference_path, "r") as reference_file:
                self.reference.add_text(reference_file.read())

            with open(cache_path, "wb") as cache_file:
                pickle.dump(self.reference, cache_file)

    def estimate_bits(self, target_path: str):
        i = 0
        total_bits = 0

        with open(target_path) as target_file:
            target_text = target_file.read()

            while i < len(target_text) - self.reference.context_size - 1:
                current_context = target_text[i:i+self.reference.context_size]
                current_symbol = target_text[i+self.reference.context_size]
                total_bits += self.reference.get_information_amount(
                    current_symbol, current_context)
                i += 1

        return ceil(total_bits)
