import os
import pandas as pd
import time
import json

# Reads the downsampled dataset
df = pd.read_csv(os.getcwd()[:os.getcwd().find("Code")] + "Data/netflix-prize/downsampled-csv/few_samples.csv")
# Gets the rating distance of each user from all the other users
print("Proceeding to get the distances from user to user")
start = time.time()
distances = {}
users = list(df["user_id"].unique())
c = 0
userss = users[:]
for a in userss:
    dist_a = {}
    df_a = df[df["user_id"] == a]
    movies_a = set(df_a["movie_id"])
    users.remove(a)
    for b in users:
        df_b = df[df["user_id"] == b]
        common_movies = movies_a & set(df_b["movie_id"])
        if common_movies:
            ratings_a = df_a[df_a["movie_id"].isin(common_movies)]["rating"].values
            ratings_b = df_b[df_b["movie_id"].isin(common_movies)]["rating"].values
            dist_a[str(b)] = str(((ratings_a - ratings_b)**2).mean()/5**2)
    distances[str(a)] = dist_a
    c += 1
    if c % 100 == 0:
        print(c, "users processed", len(userss) - c, "left")
print("This process took", round((time.time() - start)/3600, 2), "hours")  # 1.32 hours

# Saves the distances as a json: {user_a: {user_b: d_a_b, user_c: d_a_c, ...}}
print("Saving the user distances in json format")
path = os.getcwd()[:os.getcwd().find("Code")] + "Data/user-clusters/user-distances/user_"
for user in distances.keys():
    with open(path + str(user) + ".json", 'w') as fp:
        json.dump(distances[user], fp)

# Saves the clusters as a json: {user_a: user_b user_e user_j ....}
print("Saving the clusters for each user with 0.02 distance thershold")
clusters = {}
keys = []
for key, value in distances.items():
    clusters[key] = " ".join([keyy for keyy, valuee in value.items() if float(valuee) <= 0.02])
    for i in keys:
        if key in clusters[i]:
            clusters[key] += " " + str(i)
    keys.append(key)
with open(os.getcwd()[:os.getcwd().find("Code")] + "Data/user-clusters/clusters.json", "w") as fp:
    json.dump(clusters, fp)
