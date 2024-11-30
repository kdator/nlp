from typing import Tuple, List

import numpy as np
import pandas as pd

from .prefix_tree import PrefixTree

class WordCompletor:
    def __init__(self, corpus):
        """
        corpus: list – корпус текстов
        """
        words = pd.Series(corpus).explode().tolist()
        self.probabilties = dict(zip(*np.unique(words, return_counts=True)))
        self.total = sum([value for value in self.probabilties.values()])
        self.prefix_tree = PrefixTree(words)

    def get_words_and_probs(self, prefix: str) -> Tuple[List[str], List[float]]:
        """
        Возвращает список слов, начинающихся на prefix,
        с их вероятностями (нормировать ничего не нужно)
        """

        words = self.prefix_tree.search_prefix(prefix)
        probs = [self.probabilties.get(word) / self.total for word in words if word in self.probabilties]
        
        return words, probs
