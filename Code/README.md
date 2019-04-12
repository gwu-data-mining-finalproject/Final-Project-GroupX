# Code

This Readme file describes the Group Code Sections organizational structure and
use. In general there will be little discussion of software dependencies, as
throughout we're using python 3, and assuming the presence of recently updated
anaconda distribution packages.
TODO: we should probably all update our anaconda distributions and specify the
exact version here

# Running the Demo

This section describes the processes that must be completed in order to
successfully bring up our Demo GUI application.

## Collecting Data
TODO: Describe data collection process as combination of manual downloads, and
automated processes including what scripts to run, and how to organize and
stage data.

We downloaded the data from Kaggle as saved it as `.zip` files on `Data/netflix-prize` due to their massive size. The dataset was divided into 4 `.txt` files, each containing data on the following format:

```
movie_id_1
user_id_i,rating_1_i,date
user_id_j,rating_1_j,date
...
movie_id_2
....
```
We wrote a script to convert this format to `.csv` (`txt_to_csv.py`), and then we combined all 4 of them into a csv (`combine_csv.py`), which was saved as `Data/netflix-prize/complete-csv/all_samples.csv.zip`

## Preprocessing data (part of demo application or separate??)

Due to the massive size of our dataset (100,477,253 samples), we decided to trim it down substantially in order to be able to cluster the users and then run our models. First, we removed the movies and users with a small number of ratings, and then we took a random sample of the users, of size 0.05 %, ending up with 494,610 samples, saved as `Data/netflix-prize/downsampled-csv/few_samples.csv`. The code is in `user-data-preprocessing/downsample.py`. 

After doing so, we clustered the users based on the following distance metric:

$$ d(A, B) = \frac{1}{n\cdot5^2} \sum_i (r_{A_i} - r_{B_i})^2 $$

where $r_{Ai}$ is the rating of user $A$ to movie $i$, and $n$ is the number of movies both users $A$ and $B$ have rated. After computing the distance between each user, which took ...., we assigned to the same cluster all $B_j$ such as $d(A, B_j) \leq 0.04$, meaning that on average, the ratings of $A$ and $B_j$ for each common movie are within a unit distace. For example, $r_{A_i} = 5$ and $r_{B_{j_i}} = 4$. All the distances were saved in json format in `Data/user-clusters/user_distances/`, in case we want to change the threshold later on. The clusters were also saved in json format in `Data/user-clusters/clusters.json`. The code is located in `user-data-preprocessing/get_similar_users.py`. Note that a regular clustering approach like KMeans was not possible, because we would need data in the format 

| `users` | `movie_1` | `movie_2` | `movie_3` | .... |
|-------|---------|---------|---------|------|
| a     | 3       | 4       | 1       | ...  |
| b     | 2       | 2       | 5       | ...  |
| ...   | ...     | ...     | ...     | ...  |

and this would result in lots of missing values. Thus, perhaps clustering is not the most appropriate way of referring to this process, and that's why the name of the script does not allude to such term.

With the info in `Data/user-clusters/clusters.json`, a dataset like

| movie |`cluster_avg_rt` | `movie_ft_1` | `movie_ft_2` | .... | `user_A_rt`|
|-------|---------------|------------|------------|------|-----|
| `movie_1` |       |        |     | ...  |
| `movie_2`     |        |       |      | ...  |
| ...   | ...     | ...     | ...     | ...  |

can be obtained for each user `A`, and then a supervised learning model can be trained to predict the ratings of each user on new movies. The target would be `user_A_rt`, for which we will know ratings for the movies the user has rated, together with the average rating of the user's cluster for all movies and other features extracted from IMDb. 




TODO: Describe data preprocessing steps

TODO: More stuff here...
