import reflex as rx
import pandas as pd

from text_processing import WordCompletor, NGramLanguageModel, TextSuggestion

emails = pd.read_csv('handler_emails_100.csv')
corpus = emails.head(20)['message'].str.split(' ').tolist()

word_completor = WordCompletor(corpus)
ngram_model = NGramLanguageModel(corpus, n=3)
text_suggester = TextSuggestion(word_completor, ngram_model)

class State(rx.State):
    user_input: str = ""
    suggestions: list = []
    predicted_text: str = ""
    display_text: str = ""

    def update_text(self, input_text):
        self.user_input = input_text
        words = self.user_input.strip().split()
        if not words:
            self.suggestions = []
            self.predicted_text = ''
            self.display_text = ''
            return

        last_word = words[-1]
        completions, probs = word_completor.get_words_and_probs(last_word)
        if completions:
            max_prob_index = probs.index(max(probs))
            completed_word = completions[max_prob_index]
            display_words = words[:-1] + [completed_word]
            self.display_text = ' '.join(display_words)
        else:
            self.display_text = self.user_input

        predicted = text_suggester.suggest_text(words, n_words=3, n_texts=1)
        if predicted:
            self.predicted_text = ' '.join(predicted[0][len(words):])
        else:
            self.predicted_text = ''

    def select_suggestion(self, suggestion):
        self.user_input = self.user_input.strip() + ' ' + suggestion + ' '
        self.display_text = self.user_input

        self.suggestions = []
        self.predicted_text = ''
    
    def set_completed_word(self, word):
        self.user_input = word
        self.display_text = self.user_input

        self.predicted_text = ''

def index() -> rx.Component:
    return rx.container(
        rx.color_mode.button(position="top-right"),
        rx.center(
            rx.box(
                rx.vstack(
                    rx.heading("Suggester", size="9"),
                    rx.input(
                        placeholder="Your text",
                        value=State.user_input,
                        on_change=State.update_text,
                    ),
                    rx.hstack(
                        rx.text("Possible suggestions:"),
                        rx.cond(
                            State.predicted_text != '',
                            rx.button(
                                State.predicted_text,
                                on_click=lambda: State.select_suggestion(State.predicted_text)
                            ),
                            rx.text("There are no suggestions")
                        )
                    ),
                    rx.hstack(
                        rx.text("Completed text:"),
                        rx.cond(
                            State.display_text != '',
                            rx.button(
                                State.display_text,
                                on_click=lambda: State.set_completed_word(State.display_text)
                            ),
                            rx.text("There are no suggestions")
                        )
                    ),
                ),
            )
        )
    )

app = rx.App()
app.add_page(index)
