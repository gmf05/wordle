from copy import deepcopy
from wordle.utils import new_information, update_information, information_excludes_guess, update_remaining
import numpy as np
import pandas as pd


class Solver:

    def __init__(self):
        with open('five_letter_words_short.txt', 'r') as f:
            self._all_words = [w for w in f.read().split('\n') if len(w) == 5]

        self._remain_words = self._all_words.copy()
        self._information = new_information()

    def count_eliminated(self, information, remain_words):
        return sum([int(information_excludes_guess(information, word)) for word in remain_words])

    def remain_letter_frequency(self):
        return pd.value_counts([char for word in self._remain_words for char in word])

    def compute_best_guess_list(self, average='mean'):
        guess_stats = dict()
        for guess in self._remain_words:
            guess_stats[guess] = np.zeros(len(self._remain_words)).copy()

            for n, solution in enumerate(self._remain_words):
                potential_info = deepcopy(self._information)
                potential_info = update_information(potential_info, guess, solution)
                guess_stats[guess][n] = self.count_eliminated(potential_info, self._remain_words)

        # find which word has highest avg num_eliminated
        if average == 'mean':
            eliminated_words_by_guess = pd.DataFrame(guess_stats, index=self._remain_words).mean(axis=0).sort_values(ascending=False).round(1)
        elif average == 'median':
            eliminated_words_by_guess = pd.DataFrame(guess_stats, index=self._remain_words).median(axis=0).sort_values(ascending=False).round(1)

        return eliminated_words_by_guess

    def compute_best_guess(self, average='mean'):
        eliminated_words_by_guess = self.compute_best_guess_list(average=average)
        num_remaining = len(self._remain_words)
        best_guess = eliminated_words_by_guess.index.values[0]
        expected_remaining = round(num_remaining - eliminated_words_by_guess.values[0], 1)
        return best_guess, expected_remaining

    def update_information(self, information):
        self._information = information.copy()

    def update_remaining_words(self):
        self._remain_words = [word for word in self._remain_words if not information_excludes_guess(self._information, word)]



