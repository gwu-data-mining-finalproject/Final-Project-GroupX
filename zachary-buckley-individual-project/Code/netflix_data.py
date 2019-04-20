import os
import zipfile
import pandas as pd
import numpy as np
import array

## written by me to support gui decompress operation
def default_progress_handler(percentage):
    """
    function for printing out progress
    :param percentage: percent complete
    """
    print('decompressing files: ' + str(percentage))

## written by me to support gui decompress operation
def decompress(data_dir, progress_handler=default_progress_handler):
    """
    function for decompressing the zip files provided by kaggle for the
    netflix prize combined datasets
    :param data_dir: path to the Data directory
    :param progress_handler: function for printing/tracking progress (supports gui integration)
    """
    netflix_path = os.path.join(data_dir, 'netflix-prize')
    print('netflix path: ', netflix_path)
    files = os.listdir(netflix_path)
    for i in range(0, len(files)):
        if files[i].endswith('zip') and files[i].startswith('combined'):
            with zipfile.ZipFile(os.path.join(netflix_path, files[i]), "r") as zip_ref:
                zip_ref.extractall(netflix_path)
        progress_handler(int((i+1)/len(files)*100))
    progress_handler(100)

# borrowed from: https://maciejkula.github.io/2015/02/22/incremental-construction-of-sparse-matrices/
#  to avoid inefficiencies in sparse matrix libraries
#  modified heavily to apply to creating dataframes instead.
#  applied similar techniques for faster operations in a number of places
class IncrementalDataFrame(object):
    """
    Class that supports the aggregation of movie_id, user_id, rating data
    more quickly than incrementally building a dataframe row by row.
    """

    def __init__(self):

        self.movie_ids = array.array('i')
        self.user_ids = array.array('i')
        self.ratings = array.array('i')
        # array doesn't support string... so use list for dates
        # TODO: should we convert to seconds since X instead?
        # TODO: should we even worry about dates?
        # TODO: Leaving dates our for now... should be faster
        #self.date = []

    def append(self, mid, uid, r):
        self.movie_ids.append(mid)
        self.user_ids.append(uid)
        self.ratings.append(r)
        #self.date.append(d)

    def todf(self):
        movie_ids = np.frombuffer(self.movie_ids, dtype=np.int32)
        user_ids = np.frombuffer(self.user_ids, dtype=np.int32)
        ratings = np.frombuffer(self.ratings, dtype=np.int32)

        return pd.DataFrame({
            'movie_id': movie_ids,
            'user_id': user_ids,
            'rating': ratings
        })

    def __len__(self):

        return len(self.data)

## original algorithm written by Pedro (see txt_to_csv.py), then subsequently
## optimized/modified by me based on stackoverflow posts
def load_from_txt(data_dir, progress_handler=default_progress_handler):
    """
    Function to load single dataframe for txt contents of netflix data
    :param data_dir: path to the Data directory
    :param progress_handler: function responsible for feeding progress updates back to gui
    :return: pandas dataframe containing all netflix data (except ratings dates)
    """
    path = os.path.join(data_dir, "netflix-prize")
    acc = IncrementalDataFrame()
    num_movies = 17770
    #num_users = 480189
    progress_step = int(num_movies*0.01)
    movie_count = 0
    for fl in ["combined_data_1.txt", "combined_data_2.txt", "combined_data_3.txt", "combined_data_4.txt"]:
        with open(os.path.join(path, fl), "r") as s:
            line = s.readline().strip()
            current_movie_id = -1
            while line:
                if line.endswith(':'):
                    current_movie_id = int(line.strip()[:-1])
                    movie_count += 1
                    if movie_count % progress_step == 0:
                        progress_handler(int(movie_count/num_movies*100))
                else:
                    tokens = line.split(",")
                    user_id = int(tokens[0])
                    rating = int(tokens[1])
                    acc.append(current_movie_id, user_id, rating)
                line = s.readline().strip()
    progress_handler(100)

    return acc.todf()