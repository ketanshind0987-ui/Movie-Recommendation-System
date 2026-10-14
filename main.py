import csv
import os
import random

from kivy.app import App
from kivy.metrics import dp
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.spinner import Spinner
from kivy.uix.button import Button
from kivy.uix.textinput import TextInput
from kivy.uix.scrollview import ScrollView

try:
    from sklearn.feature_extraction.text import TfidfVectorizer
    from sklearn.metrics.pairwise import cosine_similarity
    NLP_AVAILABLE = True
except Exception:
    NLP_AVAILABLE = False


def load_movies():
    path = os.path.join(os.path.dirname(__file__), "movies.csv")
    movies = []
    with open(path, newline="", encoding="utf-8") as file:
        for row in csv.DictReader(file):
            movies.append(row)
    return movies


class MovieFlixApp(App):
    def build(self):
        self.title = "MovieFlix"
        self.movies = load_movies()
        root = BoxLayout(orientation="vertical", padding=dp(16), spacing=dp(10))

        heading = Label(
            text="[b]MOVIEFLIX[/b]\\nMovie Recommendation System",
            markup=True, font_size="24sp", size_hint_y=None, height=dp(80),
            color=(0.95, 0.3, 0.25, 1)
        )
        root.add_widget(heading)

        root.add_widget(Label(text="Choose a genre", size_hint_y=None, height=dp(28)))
        genres = sorted(set(movie["genre"] for movie in self.movies))
        self.genre_spinner = Spinner(
            text=genres[0], values=genres, size_hint_y=None, height=dp(48)
        )
        root.add_widget(self.genre_spinner)

        root.add_widget(Label(text="Number of recommendations (1–10)", size_hint_y=None, height=dp(28)))
        self.count_input = TextInput(
            text="5", multiline=False, input_filter="int",
            size_hint_y=None, height=dp(48), halign="center"
        )
        root.add_widget(self.count_input)

        recommend_button = Button(
            text="Recommend Movies", size_hint_y=None, height=dp(52),
            background_normal="", background_color=(0.85, 0.12, 0.18, 1)
        )
        recommend_button.bind(on_press=self.recommend)
        root.add_widget(recommend_button)

        self.result_label = Label(
            text="Choose a genre, then tap Recommend Movies.",
            size_hint_y=None, halign="left", valign="top",
            text_size=(None, None), markup=True
        )
        self.result_label.bind(texture_size=self._resize_result)
        scroll = ScrollView()
        scroll.add_widget(self.result_label)
        root.add_widget(scroll)

        root.add_widget(Label(
            text="Starter dataset • Add more titles in movies.csv",
            size_hint_y=None, height=dp(26), font_size="12sp"
        ))
        return root

    def _resize_result(self, instance, size):
        instance.height = max(size[1] + dp(20), dp(100))
        instance.text_size = (instance.width, None)

    def recommend(self, _button):
        genre = self.genre_spinner.text
        try:
            count = int(self.count_input.text or "5")
        except ValueError:
            count = 5
        count = max(1, min(10, count))

        candidates = [m for m in self.movies if m["genre"].lower() == genre.lower()]
        if not candidates:
            self.result_label.text = "No movies found for this genre yet."
            return

        if NLP_AVAILABLE and len(candidates) > 1:
            descriptions = [m["title"] + " " + m["description"] for m in candidates]
            matrix = TfidfVectorizer(stop_words="english").fit_transform(descriptions)
            similarity = cosine_similarity(matrix)
            # Pick a varied starting item, then rank related candidates against it.
            seed = random.randrange(len(candidates))
            ranked = sorted(
                range(len(candidates)),
                key=lambda idx: similarity[seed, idx],
                reverse=True
            )
            ordered = [candidates[idx] for idx in ranked]
        else:
            ordered = candidates[:]
            random.shuffle(ordered)

        output = "[b]Recommended in " + genre + ":[/b]\\n\\n"
        for index, movie in enumerate(ordered[:count], start=1):
            output += f"[b]{index}. {movie['title']}[/b]\\n{movie['description']}\\n\\n"
        if not NLP_AVAILABLE:
            output += "[i]Basic genre matching is active. Install scikit-learn for TF-IDF similarity.[/i]"
        self.result_label.text = output


if __name__ == "__main__":
    MovieFlixApp().run()
