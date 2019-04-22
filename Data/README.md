# Data

This document describes how we organized the data we collected for the project.

## Netflix Data

We've downloaded the repackaged and compressed netflix data from kaggle, and are using [git-lfs](https://git-lfs.github.com/) to store the files in git. With [git-lfs](https://git-lfs.github.com/) installed you'll get these files with your repository on cloning it down:

* [combined_data_1.txt.zip](netflix_data/combined_data_1.txt.zip)
* [combined_data_2.txt.zip](netflix_data/combined_data_2.txt.zip)
* [combined_data_3.txt.zip](netflix_data/combined_data_3.txt.zip)
* [combined_data_4.txt.zip](netflix_data/combined_data_4.txt.zip)
* [movie_titles.csv](netflix_data/movie_titles.csv)

These files will be unzipped by the [gui](../Code/README.md#Launch Graphical User Interface), loaded in, and reduced down to workable sample size. The decompressed files follow the following format:
⁠
```
movie_id_1:
user_id_i,rating_1_i,date
user_id_j,rating_1_j,date
...
movie_id_2:
....
```

The following file, which is included from the repository, was previously generated from the [gui](../Code/README.md#Launch Graphical User Interface), and contains the reduced sample:

* [few_samples.csv](netflix_data/downsampled-csv/few_samples.csv)

## User Cluster

This folder contains the user cluster data used in our Linear Regression approach.

[clusters.json](user-clusters/clusters.json) contains a list of each user from the
[few_samples.csv](netflix_data/downsampled-csv/few_samples.csv), and the user_ids
of those users that are similar. which defines the "clusters" we're using for
the Linear Regression Approach.

The distances between the users take a very long time to calculate (4-5 hours),
and as such are provided pre-computed from the git repositories. The data is stored
in [user-distances](user-clusters/user-distances).

## Documents

This folder served as document repository which performing our analysis. 
