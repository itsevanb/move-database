# Movie Database Application

A command-line Movie Database Application, which enables various operations related to movie management. 

## Features

The application has the following core functionalities:

1. **Listing all movies**: Enables users to view all movies in the database.

2. **Adding a movie**: Users can add a movie to the database. This function fetches movie details (like year of release, rating, poster URL, and plot) from the OMDB API and stores them.

3. **Deleting a movie**: Users can delete a movie from the database.

4. **Updating a movie**: Allows users to modify the rating of a movie in the database.

5. **Displaying movie statistics**: The application calculates and displays movie statistics such as the total number of movies, average and median ratings, movies with the best and worst ratings, and more.

6. **Picking a random movie**: The application can pick and display a random movie from the database.

7. **Searching for a movie**: The application supports movie searches by title, including a fuzzy match that suggests titles similar to the search query.

8. **Sorting movies by rating**: The application can sort and display all the movies in the database by their ratings.

9. **Generating a bar graph of movie ratings**: The application can generate a histogram of the distribution of movie ratings in the database.

10. **Generating a movie database webpage**: The application can generate an HTML file that displays all the movies in the database on a web page.

## Structure

The `IStorage` interface provides the contract for different storage implementations. The `StorageJson` class implements this interface and handles the persistence of movie data in a JSON file. It loads movie data from a JSON file when the application starts and saves the movie data back to the JSON file when the application ends. Similarly, the `StorageCsv` class implements the `IStorage` interface and allows handling the persistence of movie data in a CSV file.

The `MovieApp` class uses the storage class methods (`StorageJson` or `StorageCsv`) to manipulate the movie data based on user's menu choices. The menu is implemented in a loop within the `run` method of the `MovieApp` class. The menu prompts the user for actions until they choose to exit the application.

The `main` function is the application's entry point. It creates a storage object (`StorageJson` or `StorageCsv`) and a `MovieApp` object, and then runs the application.

## Usage

To run the application, navigate to the directory where the files are located and execute the `main.py` file.
The user will then be prompted to interact with the application's menu.

## Requirements

The following libraries are required:

- `requests`
- `json`
- `csv`
- `random`
- `matplotlib`
- `rapidfuzz`
- `abc`
