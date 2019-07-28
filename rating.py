import pandas as pd
import matplotlib.pyplot as plt
plt.style.use('ggplot')
from collections import OrderedDict
import warnings
warnings.filterwarnings("ignore")

r_cols = ['user_id', 'movie_id', 'rating', 'timestamp']
ratings = pd.read_csv("ratings.dat", sep="::", names=r_cols)

m_cols = ['movie_id', 'title', 'genres']
movies = pd.read_csv("movies.dat", sep="::", names=m_cols)
genres = set()
for m in movies.genres:
    genres.update(g for g in m.split('|'))
genres = sorted(genres)
for genre in genres:
    movies[genre] = [genre in genres2.split('|') for genres2 in movies.genres]

genres_info = {}
for genre in genres:
    idx = movies.index[movies[genre] == True]
    tmp = movies.loc[idx]
    count = tmp.shape[0]
    genres_info[genre] = []
    genres_info[genre].append(count)
    mean_rating = ratings.loc[ratings.movie_id.isin(tmp.movie_id), 'rating'].mean()
    genres_info[genre].append(mean_rating)

plt.figure(figsize=(8, 7))
genres_info = OrderedDict(genres_info)
count = [_[0] for _ in genres_info.values()]
mean_rating = [_[1] for _ in genres_info.values()]
bar = plt.bar(range(0, len(genres_info)), count)
plt.xticks(range(0, len(genres_info)), genres_info.keys())
ax = plt.gca()
for tick in ax.get_xticklabels():
    tick.set_rotation(75)
plt.show()

plt.figure(figsize=(8, 7))
plt.plot(range(0, len(genres_info)), mean_rating)
plt.xticks(range(0, len(genres_info)), genres_info.keys())
ax = plt.gca()
for tick in ax.get_xticklabels():
    tick.set_rotation(75)
plt.show()
