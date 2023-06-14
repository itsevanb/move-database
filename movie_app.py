import requests
import random
from rapidfuzz import fuzz
import matplotlib.pyplot as plt
from storage_json import StorageJson

class Colors:
    Blue = '\033[94m'
    Green = '\033[92m'
    Red = '\033[91m'
    Yellow = '\033[93m'
    Purple = '\033[35m'
    End = '\033[0m'

class MovieApp:
    def __init__(self, storage):
        self.storage = storage
        self.colors = Colors()

    def menu_choice(self):
        try:
            print(f'\n{self.colors.Blue}Movie Menu:{self.colors.End}')
            print('0. Exit the application')
            print('1. List all movies')
            print('2. Add movie')
            print('3. Delete movie')
            print('4. Update movie')
            print('5. Movie Stats')
            print('6. Pick a random movie')
            print('7. Search for a movie')
            print('8. Sort movies by rating')
            print('9. Display Graph of Movies')
            print('10. Generate movie data base website')
            
            choice = int(input(f'{self.colors.Purple}\nEnter choice (0-10): {self.colors.End}'))
            if 0 <= choice <= 10:
                return choice
            else:
                print(f"{self.colors.Red}Invalid choice. Please try again with values (0-10).{self.colors.End}")
        except ValueError:
            print(f"{self.colors.Red}Invalid choice. Please try again with values (0-10).{self.colors.End}")

    def welcome(self):
        print(f"{self.colors.Green}******************Welcome to our Movie Database!*********************{self.colors.End}")
        print("\n\nPlease chose an option from our 'Movie Menu' below:")

    def movie_list(self):
        movie_dict = self.storage.list_movies()
        for title, properties in movie_dict.items():
            print(f"{title}: {properties['rating']}, {properties['year']}")

    def fetch_movie_data(self, title):
        api_key = 'a1c766c0'
        url = f"http://www.omdbapi.com/?t={title}&apikey={api_key}&plot=full"
        try:
            response = requests.get(url)
        except requests.exceptions.RequestException as e:
            print(f"{self.colors.Red}Error: {e}{self.colors.End}")
            return None
        
        data = response.json()
        if data['Response'] == 'True':
            movie_data = {'title': data['Title'],
                          'year': data['Year'],
                          'rating': data['imdbRating'],
                          'poster': data['Poster'],
                          'plot': data['Plot'],}
            return movie_data
        else:
            print(f"{self.colors.Red}Error: {data['Error']}{self.colors.End}")
            return None
        
    def add_movie(self):
        title = input(f"{self.colors.Purple}Enter movie title: {self.colors.End}")
        movie_data = self.fetch_movie_data(title)
        if movie_data:
            self.storage.add_movie(movie_data['title'], movie_data['year'], movie_data['rating'], movie_data['poster'], movie_data['plot'])
            print(f"{self.colors.Green}Movie added successfully!{self.colors.End}")
        else:
            print(f"{self.colors.Red}Movie not added.{self.colors.End}")
            self.add_movie()

    def delete_movie(self):
        title = input(f"{self.colors.Purple}Please enter the movie title you would like to delete: {self.colors.End}")
        if self.storage.delete_movie(title):
            print(f"{self.colors.Green} '{title}' deleted successfully!{self.colors.End}")
        else:
            print(f"{self.colors.Red}Movie not found in database.{self.colors.End}")

    def update_movie(self):
        title = input(f"{self.colors.Purple}Please enter the movie title you would like to update: {self.colors.End}")
        rating = input(f"{self.colors.Purple}Please enter the new rating: {self.colors.End}")
        if self.storage.update_movie(title, rating):
            print(f"{self.colors.Green} '{title}' updated successfully!{self.colors.End}")
        else:
            print(f"{self.colors.Red}Movie not found in database.{self.colors.End}")
    
    def movie_stats(self):
        movie_dict = self.storage.list_movies()
        if not movie_dict:
            print(f"{self.colors.Red}No movies in database.{self.colors.End}")
        # Ratings are converted to float only if they represent a valid number
        ratings = [float(properties['rating']) for properties in movie_dict.values() if properties['rating'].replace('.', '', 1).isdigit()]
        total_movies = len(ratings)
        if total_movies == 0:  # Add this check to prevent ZeroDivisionError
            print(f"{self.colors.Red}No valid ratings found.{self.colors.End}")
            return
        average_rating = sum(ratings) / total_movies
        sorted_ratings = sorted(ratings)
        med_rating = (sorted_ratings[(total_movies - 1) // 2] + sorted_ratings[total_movies // 2]) / 2
        best_rating = max(ratings)
        worst_rating = min(ratings)
        best_movies = [title for title, properties in movie_dict.items() if properties['rating'].replace('.', '', 1).isdigit() and float(properties['rating']) == best_rating]
        worst_movies = [title for title, properties in movie_dict.items() if properties['rating'].replace('.', '', 1).isdigit() and float(properties['rating']) == worst_rating]
        print(f"{self.colors.Green}Total movies: {total_movies}{self.colors.End}")
        print(f"{self.colors.Green}Average rating: {average_rating}{self.colors.End}")
        print(f"{self.colors.Green}Median rating: {med_rating}{self.colors.End}")
        print("Best movie(s):")
        for movie in best_movies:
            print(f"{self.colors.Green}{movie}{self.colors.End}")
        print("Worst movie(s):")
        for movie in worst_movies:
            print(f"{self.colors.Red}{movie}{self.colors.End}")

        
    def random_movie(self):
        movies_dict = self.storage.list_movies()
        title = random.choice(list(movies_dict.keys()))
        movie_properties = movies_dict[title]
        print(f"{self.colors.Green}Movie: {title}{self.colors.End}")

    def search_movie(self, movie_dict, search_query):
        search_query_lower = search_query.lower()
        matching_movies = [title for title, properties in movie_dict.items() if fuzz.partial_ratio(search_query_lower, title.lower()) >= 80]
        exact_match = [title for title, properties in movie_dict.items() if fuzz.partial_ratio(search_query_lower, title.lower()) == 100]
        if exact_match:
            print(f"{self.colors.Green}Movie found: {exact_match[0]}{self.colors.End}")
        elif matching_movies:
            print(f"The movie '{search_query}' was not found. Did you mean: ")
            for title in matching_movies:
                print(f"{self.colors.Green}{title}{self.colors.End}")
        else:
            print(f"{self.colors.Red}Movie not found.{self.colors.End}")

    def graph_movie(self, movie_dict, file_name):
        ratings = [float(properties['rating']) for properties in movie_dict.values()]
        bins = range(0, 11)
        plt.hist(ratings, bins, color='green', edgecolor='black', linewidth=1.2)
        plt.xlabel('Rating')
        plt.ylabel('Frequency')
        plt.title('Movie Ratings')
        plt.xticks
        plt.tight_layout()
        plt.savefig(file_name)
        plt.show()

    def movie_rating(self, movie_dict):
        sorted_movies = sorted(movie_dict.items(), key=lambda x: float(x[1]['rating']), reverse=True)
        for title, properties in sorted_movies:
            print(f"{self.colors.Green}{title}: {properties['rating']}{self.colors.End}")

    def save_movies(self):
        self.storage.save_movies()

    def generate_html(self, movie_dict):
        with open('index.html', 'r') as file:
            index_html = file.read()
        movie_grid = ''
        for title, properties in movie_dict.items():
            if 'poster' in properties and properties['poster'] != 'N/A':
                img_tag = f'<img class="img-fluid" src="{properties["poster"]}" alt="{title}" width=200px>'
            else:
                img_tag = f'<p> No poster available </p>'
            if "plot" in properties and properties["plot"] != "N/A":
                plot = properties["plot"].replace('"', '&quot;').replace("'", "&apos;")
            else:
                plot = 'No plot available'
            movie_grid += f"""
            <div class='col-lg-4 col-md-6 col-sm-12'>
                <div class='card mb-4 shadow-sm tooltip' title='{plot}'>
                    <div class='card-header'>
                        <strong>{title}</strong> ({properties['year']})
                    </div>
                    <div class='card-body'>
                        {img_tag}
                    </div>
                    <div class='card-footer'>
                        Rating: {properties['rating']}
                    </div>
                </div>
            </div>"""

        html_content = index_html.replace("__TEMPLATE_TITLE__", "Movie Database")
        html_content = html_content.replace("__TEMPLATE_MOVIE_GRID__", movie_grid)
        return html_content

    def run(self):
        self.welcome()
        while True:
            choice = self.menu_choice()
            if choice == 1:
                self.movie_list()
            elif choice == 2:
                self.add_movie()
            elif choice == 3:
                self.delete_movie()
            elif choice == 4:
                self.update_movie()
            elif choice == 5:
                self.movie_stats()
            elif choice == 6:
                self.random_movie()
            elif choice == 7:
                search_query = input(f"{self.colors.Purple}Please enter the movie title to search: {self.colors.End}")
                self.search_movie(self.storage.list_movies(), search_query)
            elif choice == 8:
                self.movie_rating(self.storage.list_movies())
            elif choice == 9:
                file_name = input(f"{self.colors.Purple}Please enter the file name: {self.colors.End}")
                self.graph_movie(self.storage.list_movies(), file_name)
            elif choice == 10:
                html_content = self.generate_html(self.storage.list_movies())
                with open('ouput.html', 'w') as file:
                    file.write(html_content)
                print(f"{self.colors.Green}HTML file generated successfully!{self.colors.End}")
            elif choice == 0:
                self.save_movies()
                print(f"{self.colors.Green}Movies saved successfully!{self.colors.End}")
                break

if __name__ == '__main__':
    storage = StorageJson('movies.json')
    app = MovieApp(storage)
    app.run()