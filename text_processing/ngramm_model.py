from typing import Tuple, List
from collections import defaultdict

class NGramLanguageModel:
    def __init__(self, corpus, n):
        self.n = n
        self.ngrams = defaultdict(list)

        self._initialize_model(corpus)

    def _initialize_model(self, corpus):
        for sentence in corpus:
            sent_len = len(sentence)
            for i in range(sent_len):
                for j in range(1, sent_len - i + 1):
                    prefix = tuple(sentence[i:i + j - 1])
                    next_word = sentence[i + j - 1]
                    self.ngrams[prefix].append(next_word)

    def get_next_words_and_probs(self, prefix: List[str]) -> Tuple[List[str], List[float]]:
        """
        Возвращает список слов, которые могут идти после prefix, 
        а также список вероятностей этих слов.
        """
        next_words = self.ngrams.get(tuple(prefix), [])
        next_words_len = len(next_words)

        words = [word for word in next_words]
        probs = [next_words.count(word) / next_words_len for word in next_words]

        return words, probs
