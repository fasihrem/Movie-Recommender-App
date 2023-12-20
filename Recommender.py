import pandas as pd
import numpy as np
from sklearn.neighbors import NearestNeighbors

movies = pd.read_csv('movies.csv', sep=';', encoding='latin-1').drop('Unnamed: 3', axis=1)
ratings = pd.read_csv('ratings.csv', sep=';')
users = pd.read_csv('users.csv', sep=';')
rating_pivot = ratings.pivot_table(values='rating',columns='userId',index='movieId').fillna(0)

nn_algo = NearestNeighbors(metric='cosine')
nn_algo.fit(rating_pivot)


class Recommender:
    def __init__(self):
        # This list will stored movies that called atleast ones using recommend_on_movie method
        self.hist = []
        self.ishist = False  # Check if history is empty

    # This method will recommend movies based on a movie that passed as the parameter
    def recommend_on_movie(self, movie, n_reccomend=5):
        self.ishist = True
        movieid = int(movies[movies['title'] == movie]['movieId'])
        self.hist.append(movieid)
        distance, neighbors = nn_algo.kneighbors([rating_pivot.loc[movieid]], n_neighbors=n_reccomend + 1)
        movieids = [rating_pivot.iloc[i].name for i in neighbors[0]]
        recommeds = [str(movies[movies['movieId'] == mid]['title']).split('\n')[0].split('  ')[-1] for mid in movieids
                     if mid not in [movieid]]
        return recommeds[:n_reccomend]

    # This method will recommend movies based on history stored in self.hist list
    def recommend_on_history(self, n_reccomend=5):
        if self.ishist == False:
            return print('No history found')
        history = np.array([list(rating_pivot.loc[mid]) for mid in self.hist])
        distance, neighbors = nn_algo.kneighbors([np.average(history, axis=0)],
                                                 n_neighbors=n_reccomend + len(self.hist))
        movieids = [rating_pivot.iloc[i].name for i in neighbors[0]]
        recommeds = [str(movies[movies['movieId'] == mid]['title']).split('\n')[0].split('  ')[-1] for mid in movieids
                     if mid not in self.hist]
        return recommeds[:n_reccomend]