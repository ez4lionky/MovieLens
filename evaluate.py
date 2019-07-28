import operator
from functools import reduce
import warnings
warnings.filterwarnings("ignore")
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
plt.style.use('ggplot')
from collections import Counter
pd.set_option('display.max_columns', None)

u_cols = ['user_id', 'gender', 'age', 'occupation', 'zip_code']
users = pd.read_csv("users.dat", sep="::", names=u_cols)
# labels = ["Children", "Teenagers", "Middle-aged", "Elder"]  # 1(under 18), 18-34(18, 25), 35-50(35, 45), 50-(50, 56)
# users['age_group'] = pd.cut(users.age, [0, 18, 35, 50, 100], labels=labels, right=False)
labels = [0, 1, 4, 7, 17]

r_cols = ['user_id']
for i in range(10):
    r_cols.append("top" + str(i))
recomm = pd.read_csv("user_recomm.csv", names=r_cols)
users_recomm = pd.merge(users, recomm)

m_cols = ['movie_id', 'title', 'genres']
movies = pd.read_csv("movies.dat", sep="::", names=m_cols)
genres = set()
for m in movies.genres:
    genres.update(g for g in m.split('|'))
genres = sorted(genres)
users_recomm['all_genres'] = ''

for i in range(10):
    users_recomm["top" + str(i)] = users_recomm["top" + str(i)].map(movies.set_index('movie_id').genres).fillna('')
    if i == 9:
        users_recomm['all_genres'] = users_recomm['all_genres'] + users_recomm["top" + str(i)]
    else:
        users_recomm['all_genres'] = users_recomm['all_genres'] + users_recomm["top" + str(i)] + "|"
    users_recomm = users_recomm.drop("top" + str(i), axis=1)

for genre in genres:
    users_recomm[genre] = [Counter(movie.split('|'))[genre] for movie in users_recomm.all_genres]
users_recomm = users_recomm.drop('all_genres', axis=1)
# groups = users_recomm.groupby('age_group')
groups = users_recomm.groupby('occupation')
i = 0
xticks = []
bars = []
plt.figure(figsize=(8, 7))
n = 3
ratios = []
for c in labels:
    g = groups.get_group(c)
    print(len(g))
    genre_sum = g.loc[:, genres].apply(sum).to_dict()
    top = sorted(zip(genre_sum.values(), genre_sum.keys()))[-n:]
    top_count = [_[0] for _ in top]
    top_index = [(_[1], c) for _ in top]
    xticks.append(top_index)
    start = i * n
    bars.append(plt.bar(range(start, start + n), top_count))
    top_ratio = [_ / (len(g) * 10) for _ in top_count]
    ratios.append(top_ratio)
    # plt.plot(range(start, start + n), top_ratio)
    i += 1

labels = ["other", "academic/educator", "college/grad student", "executive/managerial", "technician/engineer"]
plt.legend(bars, labels)
xticks = reduce(operator.add, xticks)
plt.xticks(range(0, i * n), xticks)
ax = plt.gca()
for tick in ax.get_xticklabels():
    tick.set_rotation(75)
plt.show()

plt.figure()
plots = []
i = 0
for ratio in ratios:
    plots.append(plt.plot(range(0, n), ratio, label=labels[i]))
    i += 1

plt.legend()
plt.xticks(range(0, n), ["Top" + str(i + 1) for i in range(n)])
plt.show()

# teenagers = groups.get_group("Teenagers")
# middle_aged = groups.get_group("Middle-aged")
# print(teenagers.loc[:, ["top" + str(i) for i in range(3)]])

