import pandas as pd
import os
import json


# Reads the json with all the clusters for each user
path = os.getcwd()[:os.getcwd().find("Code")] + "/Data/user-clusters/clusters.json"
with open(path, "r") as s:
    clusters = json.loads(s.read())

# Gets the cluster of users for user 2451020
similar_users_to_2451020 = [int(user) for user in clusters["2451020"].split()] + [2451020]

# Reads the downsampled dataframe and gets the data for the users in user 2451020 cluster, including itself
df = pd.read_csv(os.getcwd()[:os.getcwd().find("Code")] + "/Data/netflix-prize/downsampled-csv/few_samples.csv", index_col=0)
df_2451020 = df[df["user_id"].isin(similar_users_to_2451020)]

# Example of how to get the DataFrame to be augmented with IMDb data 
# (add features for each movie) and then to be used to train our models
movie_ids = []
movies_avg_rating = []
user_2451020_ratings = []
for movie_id in df_2451020["movie_id"].unique():
    movie_ids.append(movie_id)
    movies_avg_rating.append(df_2451020[df_2451020["movie_id"] == movie_id]["rating"].mean())
    try:
        user_2451020_ratings.append(df_2451020[(df_2451020["movie_id"] == movie_id) & (df_2451020["user_id"] == 2451020)]["rating"].iloc[0])
    except IndexError:
        user_2451020_ratings.append("?")
    
print(pd.DataFrame({"movie_id": movie_ids, "cluster_avg_rating": movies_avg_rating, "user_2451020_rating": user_2451020_ratings}).head())