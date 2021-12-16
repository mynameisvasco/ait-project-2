from math import ceil
from fcm import Fcm
from pathlib import Path
import pickle


class Lang:
    reference: Fcm
    name: str

    def __init__(self, reference_path: str) -> None:
        reference_path_base = reference_path.split('/')[-1]
        self.name = reference_path_base.split(".")[0]
        cache_path = Path(f"cache/{reference_path_base}.cache")

        if cache_path.exists():
            with open(cache_path, "rb") as cache_file:
                self.reference = pickle.load(cache_file)
        else:
            self.reference = Fcm(0.05, 5)

            with open(reference_path, "r") as reference_file:
                reference_text = reference_file.read()
                self.reference.add_text(reference_text)

            with open(cache_path, "wb") as cache_file:
                pickle.dump(self.reference, cache_file)

    def sum_estimate_bits(self, target_text: str):
        total_bits = 0

        for i in range(len(target_text) - self.reference.context_size):
            current_context = target_text[i:i +
                                          self.reference.context_size]
            current_symbol = target_text[i+self.reference.context_size]
            total_bits += self.reference.get_information_amount(
                current_symbol, current_context)

        return ceil(total_bits)

    def list_estimate_bits(self, target_text: str):
        total_bits = []

        for i in range(len(target_text) - self.reference.context_size):
            current_context = target_text[i:i +
                                          self.reference.context_size]
            current_symbol = target_text[i+self.reference.context_size]
            bits = ceil(self.reference.get_information_amount(
                current_symbol, current_context))
            total_bits.append(bits)

        return total_bits
