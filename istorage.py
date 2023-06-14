from abc import ABC, abstractmethod

class IStorage(ABC):
    """
    An abstract base class that provides a contract for different storage mediums.
    The storage class should be able to list, add, delete, and update movies.
    """

    @abstractmethod
    def list_movies(self):
        """
        Returns a list of all movies stored.
        
        """
        pass

    @abstractmethod
    def add_movie(self, title, year, rating, poster, plot):
        """
        Adds a new movie to the storage.
        
        Parameters:
        title (str): The title of the movie.
        year (int): The year the movie was released.
        rating (float): The rating of the movie out of 10.
        poster (str): The URL of the movie poster.
        plot (str): A short description of the movie plot.
        
        Returns:
        dict: A dictionary representing the movie that was added.
        """
        pass

    @abstractmethod
    def delete_movie(self, title):
        """
        Deletes a movie from the storage.
        
        Parameters:
        title (str): The title of the movie to be deleted.
        
        Returns:
        bool: True if the movie was successfully deleted, False otherwise.
        """
        pass

    @abstractmethod
    def update_movie(self, title, rating):
        """
        Updates the rating of a movie.
        
        Parameters:
        title (str): The title of the movie to be updated.
        rating (float): The new rating of the movie.
        
        Returns:
        dict: A dictionary representing the updated movie.
        """
        pass
