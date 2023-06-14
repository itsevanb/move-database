import csv
from istorage import IStorage

class StorageCsv(IStorage):
    def __init__(self, filepath):
        self.filepath = filepath

    def _load_movies(self):
        try:
            with open(self.filepath, mode='r') as csv_file:
                return list(csv.DictReader(csv_file))
        except FileNotFoundError:
            return {}

    def _save_movies(self, movies):
        if not movies:
            return
        with open(self.filepath, mode='w', newline='') as csv_file:
            writer = csv.DictWriter(csv_file, fieldnames=movies[0].keys())
            writer.writeheader()
            writer.writerows(movies)

    def list_movies(self):
        return self._load_movies()

    def add_movie(self, title, year, rating, poster, plot):
        movies = self._load_movies()
        new_movie = {'title': title, 'year': year, 'rating': rating, 'poster': poster, 'plot': plot}
        movies.append(new_movie)
        self._save_movies(movies)
        return new_movie

    def delete_movie(self, title):
        movies = self._load_movies()
        movies = [movie for movie in movies if movie['title'] != title]
        self._save_movies(movies)
        return not any(movie['title'] == title for movie in movies)

    def update_movie(self, title, rating):
        movies = self._load_movies()
        for movie in movies:
            if movie['title'] == title:
                movie['rating'] = rating
        self._save_movies(movies)
        return next((movie for movie in movies if movie['title'] == title), None)