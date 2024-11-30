from typing import Union

class TextSuggestion:
    def __init__(self, word_completor, n_gram_model):
        self.word_completor = word_completor
        self.n_gram_model = n_gram_model

    def suggest_text(self, text: Union[str, list], n_words=3, n_texts=1) -> list[list[str]]:
        """
        Возвращает возможные варианты продолжения текста (по умолчанию только один)
        
        text: строка или список слов – написанный пользователем текст
        n_words: число слов, которые дописывает n-граммная модель
        n_texts: число возвращаемых продолжений (пока что только одно)
        
        return: list[list[srt]] – список из n_texts списков слов, по 1 + n_words слов в каждом
        Первое слово – это то, которое WordCompletor дополнил до целого.
        """

        words = text.strip().split() if isinstance(text, str) else text[:]
        if not words:
            return []

        last_word = words[-1]
        completions, probs = self.word_completor.get_words_and_probs(last_word)
        completed_word = max(zip(completions, probs), key=lambda x: x[1], default=(last_word, 0))[0]

        full_words = words[:-1] + [completed_word]
        context = full_words[-(self.n_gram_model.n - 1):]

        suggestion = [completed_word]
        for _ in range(n_words):
            next_words, next_probs = self.n_gram_model.get_next_words_and_probs(context)
            if not next_words:
                break
            next_word = max(zip(next_words, next_probs), key=lambda x: x[1])[0]
            suggestion.append(next_word)
            context = context[1:] + [next_word]

        return [suggestion]