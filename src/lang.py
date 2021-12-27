from math import ceil
from fcm import Fcm
from pathlib import Path
import pickle


class Lang:
    reference_chars: int
    reference: Fcm
    name: str

    def __init__(self, reference_path: str, reference_chars: int) -> None:
        reference_path_base = reference_path.split('/')[-1]
        self.reference_chars = reference_chars
        self.name = reference_path_base.split(".")[0]
        cache_path = Path(
            f"cache/{reference_path_base}_{reference_chars}.cache")

        if cache_path.exists():
            with open(cache_path, "rb") as cache_file:
                self.reference = pickle.load(cache_file)
        else:
            self.reference = Fcm(0.05, 5)

            with open(reference_path, "r") as reference_file:
                reference_text = reference_file.read()
                if self.reference_chars and self.reference_chars <= len(reference_text):
                    reference_text = reference_text[:self.reference_chars]

                self.reference.add_text(reference_text)

            with open(cache_path, "wb") as cache_file:
                pickle.dump(self.reference, cache_file)

    def estimate_bits(self, context: str, symbol: str):
        return self.reference.get_information_amount(symbol, context)
