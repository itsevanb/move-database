import json
from istorage import IStorage


class StorageJson(IStorage):
    def __init__(self, file_path):
        """
        Initialize a new instance of Storage.
        Parameters:
        file_path (str): The path to the file where the movies are stored.
        
        """
        self.file_path = file_path
        self.movies = self.load_movies()

    def load_movies(self):
        """
        Load the movies from the file at the specified path.
        Returns:
        dict: A dictionary mapping movie titles to movie details.
        """
        try:
            with open(self.file_path, 'r') as file:
                movies = json.load(file)
        except FileNotFoundError:
            movies = {}
        return movies
    
    def save_movies(self):
        """
        Save current state of the movies to the file at the specified path.
        
        """
        with open(self.file_path, 'w') as file:
            json.dump(self.movies, file)

    def list_movies(self):
        """
        List all movies stored.

        Returns:
        dict: A dictionary mapping movie titles to movie details.
        
        """
        return self.movies
    
    def add_movie(self, title, year, rating, poster, plot):
        """
        Add a new movie to the storage.
        Parameters:
        title (str): The title of the movie.
        year (int): The year the movie was released.
        rating (float): The rating of the movie out of 10.
        poster (str): The URL of the movie poster.
        plot (str): A short description of the movie plot.
        
        """
        self.movies[title] = {'year': year, 'rating': rating, 'poster': poster, 'plot': plot}
        self.save_movies()

    def delete_movie(self, title):
        """
        Delette a movies from the storage.
        Parameters:
        Title (str): of movie to be deleted.
        Returns:
        bool: True if the movie was successfully deleted, False otherwise.
        
        """
        if title in self.movies:
            del self.movies[title]
            self.save_movies()
            return True
        else:
            return False
        

    def update_movie(self, title, rating):
        """Update the rating of a movie.
        Parameters:
        title (str): The title of the movie to be updated.
        rating (float): The new rating of the movie.
        Returns:
        bool: True if the movie was successfully updated, False otherwise.
        """
        if title in self.movies:
            self.movies[title]['rating'] = rating
            self.save_movies()
            return True
        else:
            return False