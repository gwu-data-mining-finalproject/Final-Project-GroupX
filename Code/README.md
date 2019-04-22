# Code

This README file describes the Group Code Sections organizational structure and
use.




## Running the Demo

This section describes the processes that must be completed in order to
successfully bring up our Demo GUI application. The driver application in
the

### Python Interpreter Environment

Please use a python36 interpreter, with the following packages available:

* numpy
* pandas
* seaborn
* sklearn
* scipy
* matplotlib
* PyQt5
* zipfile
* os
* sys
* array
* time
* imdb
* operator
* json
* surprise
* warnings
* math
* gc
* datetime

*Note: All these packages are available in the default anaconda3 distribution*

### Launch Graphical User Interface

This section describes the process of starting the GUI. Ultimately both versions
of this process will execute [driver.py](../driver.py)

##### PyCharm (Cross Platform)

Create a pycharm project pointing at the 'Final-Project-GroupX' folder (root node
of the repository). Then configure the interpreter to meet the requirements
described in the [Interpreter](Python Interpreter Environment) section above.

Locate a file entitled [driver.py](../driver.py) located at the 'Final-Project-GroupX' folder
level of the repository. This is the only code file not located inside a Code
folder, and is only used to launch the gui.

Right click the file, and click `Run Driver`, which will have a green arrow next
to it. *Note: The DeprecationWarning is expected, it's caused by a library that
sklearn is dependent on*

##### Command Line (MAC, Linux)

If your using a bash shell on a Linux, or MAC computer, you can use the following
as an alternative to the instructions immediately above.

Ensure the python3 executable available in you PATH variable meets the requirements
described in the [Interpreter](Python Interpreter Environment) section above.

Then in a terminal, navigate to the `Final-Project-GroupX` folder, such that executing the following command will give you back `Final-Project-GroupX` in response. *NOTE:
if you renamed the repository when cloning it down, the response should match the
name you used*

```bash
basename `pwd`
```

Then execute the following command to launch the gui:

```bash
python3 driver.py
```
*Note: The DeprecationWarning is expected, it's caused by a library that
sklearn is dependent on*

### Operating the GUI

This section Describes the GUI's operation

The GUI will allow you to resample the dataset.

*NOTE: Some of the model analysis code is tied to the sample data previously saved in
the repository. Some analysis processes take a long time (4-5 hours), and will need
to be rerun to analyze another sample.*

To operate the GUI simply press the buttons that are available, then the next as
they become available. The progress bars will indicate incremental progress for
each operation. Most of the GUI wiring code is located [here](gui/NetflixDataPanel.py)

#### Decompress Ratings Data

This operaion will decompress the zip files with the repackaged netflix ratings data. *NOTE: This won't be available if the files have already been decompressed in the directory* The code responsible for this operation is located [here](preprocessing/netflix_data.py).

#### Load Data

This operation will parse, and load the netflix rating data into Random Access Memory (RAM). The code responsible for this operation is located [here](preprocessing/netflix_data.py).

#### Reduce Movies

This operation will reduce the data loaded into RAM, using the specified
cutoff value as the minimum required number of ratings for a movie to stay in the
dataset. The responsible for this operation is located [here](preprocessing/downsample.py).

#### Reduce Users

This operation will reduce the data loaded into RAM, using the specified
cutoff value as the minimum required number of ratings for a user to stay in the dataset. The responsible for this operation is located [here](preprocessing/downsample.py).

#### Reduce SRSWR

This operation will reduce the dataset by applying SRSOR, using sklearns train_test_split function, and the specified random_seed value, to select .5% of the users from the data in RAM. The responsible for this operation is located [here](preprocessing/downsample.py). *NOTE: Despite the text in the GUI saying SRSWR, this operation is in fact performing Simple Random Selection Without Replacement (SRSOR).*

#### Save

Saves the reduced data from RAM into a csv formatted file, in [few_samples](../Data/netflix-prize/downsampled-csv/few_samples.csv).

## Preprocessing data

Due to the massive size of our dataset (100,477,253 samples), we decided to trim it down substantially in order to be able to cluster the users and then run our models. First, we removed the movies and users with a small number of ratings, and then we took a random sample of the users, of size 0.5 %, ending up with 510,852 samples, saved in [few_samples](../Data/netflix-prize/downsampled-csv/few_samples.csv). The code is in [downsample.py](preprocessing/downsample.py).This operation can be performed using
the GUI as described [above](Launch Graphical User Interface).

After doing so, we clustered the users based on the following distance metric:

![m](https://i.imgur.com/JPTG1DD.png)

where `rA_i` is the rating of user `A` to movie `i`, and `n` is the number of movies both users `A` and `B` have rated. After computing the distance between each user, which took one and a half hours, we assigned to the same cluster all `B_j` such as `d(A, B_j) = 0.02`, meaning that on average, the ratings of `A` and `B_j` for each common movie are within a 0.7 units of distance. For example, `rA_i = 5` and `rB_ji = 4.3`. All the distances were saved in json format in [user_distances](../Data/user-clusters/user_distances/), as we wanted to play with the threshold later on. The clusters were also saved in json format in [clusters.json](../Data/user-clusters/clusters.json). The code is located in [get\_similar\_users.py](preprocessing/get_similar_users.py). Note that a regular clustering approach like KMeans was not possible, because we would need data in the format

| `users` | `movie_1` | `movie_2` | `movie_3` | .... |
|-------|---------|---------|---------|------|
| a     | 3       | 4       | 1       | ...  |
| b     | 2       | 2       | 5       | ...  |
| ...   | ...     | ...     | ...     | ...  |

and this would result in lots of missing values. Thus, perhaps clustering is not the most appropriate way of referring to this process, and that's why the name of the script does not allude to such term.

With the info in [clusters.json](../Data/user-clusters/clusters.json), a dataset like

|   movie   |`cluster_avg_rt` | `userA_rt`|
|-----------|-----------------|------------|
| `movie_1` |                 |            |
| `movie_2` |                 |            |
| ...       | ...             | ...        |

can be obtained for each user `A`, and then a supervised learning model can be trained to predict the ratings of each user on new movies. The target would be `userA_rt`, for which we will know ratings for the movies the user has rated, together with the average rating of the user's cluster for all movies.

## Modeling

Our code for this section is located in [models](models). [models.ipynb](models/models.ipynb) contains the regression approached for each user. [collaborative_filtering.ipynb](models/collaborative_filtering.ipynb) contains the Collaborative Filtering approach. A brief comparison between the two is located on [comparison.ipynb](models/comparison.ipynb). 
