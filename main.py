from storage_json import StorageJson 
from movie_app import MovieApp  

def main():
    # Create a StorageJson object
    storage = StorageJson(input("Enter the name of the file to load: "))

    # Create a MovieApp object with the StorageJSON object
    app = MovieApp(storage)

    # Run the app
    app.run()

if __name__ == "__main__":
    main()
