
# My attempt at the Netflix Simple Recommender System code organized by class and method

# Create class SimpleNetFlixRecommender System
class SimpleNetFlixRecommender:

    # Initialization of class
    def __init__(self, movie_title, movie_id, rating, number_ratings, Correlation):
        self.movie_title = movie_title
        self.movie_id = movie_id
        self.rating = rating
        self.number_ratings = number_ratings
        self.Correlation = Correlation

    # Display correlated movie in proper sequence
    def display_movie(self):
        return '{} {} {} {} {}'.format(self.movie_title, self.movie_id, self.rating, self.number_ratings,
                                       self.Correlation)

    # Computes and outputs the movie correlations
    def movie_corr(self):
        pass

    # GUI Input for movie you watched and liked and want additional recommendations for similar correlated movies
    #   Based on user ratings - collaborative filtering
    def input_movie(self):
        pass

    # Pre-process data to ensure its clean and runs perfectly in the recommendation system
    def pre_processing(self):
        pass

    # Combine files for pre-processing
    def combine_files(self):
        pass

    # Load files and manipulate data into proper formats
    def load_files(self):
        pass


