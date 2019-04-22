import os
import operator
import pandas as pd
import time
from sklearn.model_selection import train_test_split
# import matplotlib.pyplot as plt

# Loads the massive DataFrame
start = time.time()
print("Starting the loading process")
data_path = os.getcwd()[:os.getcwd().find("Code")] + "Data/netflix-prize/complete-csv/all_samples.csv"
df = pd.read_csv(data_path)
del df["Unnamed: 0"]
del df["date"]
print("The loading process took", round(time.time() - start), "seconds")

# Gets the number of reviews per movie
n_reviews_per_movie = {}
for movie_id, count in df["movie_id"].value_counts().items():
    n_reviews_per_movie[movie_id] = count
# plt.hist(n_reviews_per_movie.values(), bins=30)
# plt.show()
print("We have", len(n_reviews_per_movie.keys()), "movies")
# Sorts the number of ratings per movie in ascending order
sorted_n_reviews_per_movie = sorted(n_reviews_per_movie.items(), key=operator.itemgetter(1))
print("The smallest number of ratings a movie has is", sorted_n_reviews_per_movie[0][1])
print("There are 2000 movies with less than", sorted_n_reviews_per_movie[2000][1], "ratings")
print("There are 5018 movies with less than", sorted_n_reviews_per_movie[5018][1], "ratings")
print("Keeping only the movies with more than 214 ratings...")
df = df[df["movie_id"].isin([movie_id[0] for movie_id in sorted_n_reviews_per_movie[5018:]])]
print("The size of the dataset has been reduced from 100477253 to", df.shape[0])

# Gets the number of reviews per user
n_reviews_per_user = {}
for user_id, count in df["user_id"].value_counts().items():
    n_reviews_per_user[user_id] = count
# plt.hist(n_reviews_per_user.values(), bins=30)
# plt.show()
print("We have", len(n_reviews_per_user.keys()), "users")
# Sorts the number of ratings per user in ascending order
sorted_n_reviews_per_user = sorted(n_reviews_per_user.items(), key=operator.itemgetter(1))
print("The smallest number of ratings a user has made is", sorted_n_reviews_per_user[0][1])
print("There are 93483 users who have made less than", sorted_n_reviews_per_user[93483][1], "ratings")
print("Keeping only the users with more than 30 ratings...")
df = df[df["user_id"].isin([user_id[0] for user_id in sorted_n_reviews_per_user[93483:]])]
print("The size of the dataset has been reduced from 99792842 to", df.shape[0])

# Gets a small random sample of the users that are left
print("Selecting a 0.5% random sample of users...")
_, small_sample_of_users = train_test_split(df["user_id"].unique(), test_size=0.005, random_state=42)
df = df[df["user_id"].isin(small_sample_of_users)]

# Saves the result to a csv
print("Saving the downsampled dataset to a csv")
df.to_csv(os.getcwd()[:os.getcwd().find("Code")] + "Data/netflix-prize/downsampled-csv/few_samples.csv")

