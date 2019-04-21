
# MOVE TO DATA DIR
We downloaded the data from Kaggle as saved it as `.zip` files in [netflix-prize](Data/netflix-prize) due to their massive size. The dataset was divided into 4 `.txt` files, each containing data on the following format:

```
movie_id_1
user_id_i,rating_1_i,date
user_id_j,rating_1_j,date
...
movie_id_2
....
```
We wrote a script to convert this format to `.csv` (`txt_to_csv.py`), and then we combined all 4 of them into a csv (`combine_csv.py`), which was saved as `Data/netflix-prize/complete-csv/all_samples.csv.zip`


### Collecting and Preprocessing Data (GUI)

We utilized [git-lfs](https://git-lfs.github.com/) to store some of our larger
files, which are available immediately after cloning the repository. These files
are generally located under the [Data](../Data/README.md) directory, but may also
be present in our individual project folders.
