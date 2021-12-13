from fcm import Fcm
from typing import Tuple, List

class CombinedFcm:
    average_window_size: int
    current_char_count: int
    fcms: Tuple[Fcm]
    fcm_weights: List[int]
    context_size: int

    def __init__(self, average_window_size: int, *fcms: Fcm):
        self.average_window_size = average_window_size
        self.current_char_count = 0
        self.fcms = fcms
        self.fcm_weights = [1/len(fcms)] * len(fcms)
        self.fcm_scores = [0] * len(fcms)
        self.context_size = fcms[0].context_size
        for fcm in fcms:
            if fcm.context_size > self.context_size:
                self.context_size = fcm.context_size

    def get_information_amount(self, symbol: str, context: str):
        assert len(context) == self.context_size

        if self.current_char_count > self.average_window_size:
            self.current_char_count = 0
            for i in range(0, len(self.fcms)):
                self.fcm_weights[i] = self.fcm_scores[i] / self.average_window_size
            self.fcm_scores = [0] * len(self.fcms)
            
        self.current_char_count += 1
        fcm_results = [fcm.get_information_amount(symbol, context[-fcm.context_size:]) for fcm in self.fcms]
        final_result = 0

        lowest_fcm_index = 0
        lowest_fcm_result = fcm_results[lowest_fcm_index]
        for i in range(0, len(self.fcms)):
            final_result += self.fcm_weights[i] * fcm_results[i]
            if fcm_results[lowest_fcm_index] < lowest_fcm_result:
                lowest_fcm_index = i
                lowest_fcm_result = fcm_results[lowest_fcm_index]
        self.fcm_scores[lowest_fcm_index] += 1

        return final_result
