import os
import pandas as pd
import numpy as np
import scipy as sc
import scipy.sparse as sp
import array
import time


## Goal here was to read ratings/movie data into a sparse matrix
## This file didn't end up getting used as we decided to go with the dataframe
## approach, since it was more familiar to us.

## Implementation uses similar optimization techniques as those in
## netflix_data.py in Code.preprocessing.
## (attempting this below is where i found/learned that technique)
def default_progress_handler(percentage):
    print('processing text: ' + str(percentage))


class UserIDMap(object):
    """
    Class responsible for dealing netflix user id to internal user id mapping
    This was necessary to 'pack' the sparse matrix more densely, as the range
    of the netflix user ids is 1 to 2649429 and there are only 480189 users in
    the combined data files.
    """
    def __init__(self):
        self.nuid_to_iuid = {}
        self.iuid_to_nuid = {}
        self.next_iuid = 0

    def create_or_get_iuid(self, nuid):
        if nuid not in self.nuid_to_iuid:
            self.nuid_to_iuid[nuid] = self.next_iuid
            self.iuid_to_nuid[self.next_iuid] = nuid
            self.next_iuid += 1

        return self.nuid_to_iuid[nuid]

    def __len__(self):
        return len(self.nuid_to_iuid)

# borrowed from: https://maciejkula.github.io/2015/02/22/incremental-construction-of-sparse-matrices/
#  to avoid inefficiencies in sparse matrix libraries
class IncrementalCOOMatrix(object):
    """
    This Class is responsible for aggregating the user rating data into c-arrays
    c-arrays are much more efficient for this task than incrementally appending
    each row of data to the dataframe, and using them drastically speeds up this
    operation, though i do any strict timing tests during development. The problem
    is that each append operation creates new dataframe objects, and performs copies
    on some if not all of the data in the dataframe. the c-array function is optimized
    to expand it's container size less frequently, and doesn't have as much overhead
    from object creation operations.
    """

    def __init__(self, shape, dtype):

        if dtype is np.int32:
            type_flag = 'i'
        elif dtype is np.int64:
            type_flag = 'l'
        elif dtype is np.float32:
            type_flag = 'f'
        elif dtype is np.float64:
            type_flag = 'd'
        else:
            raise Exception('Dtype not supported.')

        self.dtype = dtype
        self.shape = shape

        self.rows = array.array('l')
        self.cols = array.array('l')
        self.data = array.array(type_flag)

    def append(self, i, j, v):

        m, n = self.shape

        if (i >= m or j >= n):
            raise Exception('Index out of bounds')

        self.rows.append(i)
        self.cols.append(j)
        self.data.append(v)

    def tocoo(self):

        rows = np.frombuffer(self.rows, dtype=np.int64)
        cols = np.frombuffer(self.cols, dtype=np.int64)
        data = np.frombuffer(self.data, dtype=self.dtype)

        print(len(rows))
        print(len(cols))
        print(len(data))

        return sp.coo_matrix((data, (rows, cols)),
                             shape=self.shape)

    def __len__(self):

        return len(self.data)

def process_to_numpy_matrix(idmap = UserIDMap(), progress_handler=default_progress_handler):
    """
    This function is used to process the data files into a sparse matrix
    The function should likely be expanded to take in a data_dir similar to functions in
    netflix_data.py, but this was sufficient for testing out the concept.
    :param idmap: useridmap... allows for previously constructed useridmap to be reused
    :param progress_handler: function for enabling progress-bar interactions/printouts occur by default
    :return: sparse matrix
    """
    start = time.time()
    path = '/home/zbuckley/Dropbox/DataMining/Final-Project-GroupX/Data/netflix-prize'
    # initialize sparse scipy matrix
    # https://docs.scipy.org/doc/scipy/reference/generated/scipy.sparse.dok_matrix.html#scipy.sparse.dok_matrix
    #   chose dok sparse matrix as it's supposed to be optimized for incremental array construction
    # this switched to: https://maciejkula.github.io/2015/02/22/incremental-construction-of-sparse-matrices/
    #   after further experimentation..
    num_movies = 17770
    num_users = 480189
    #TODO: added buffer on size, as numbers above seem to be incorrect???
    ratings = IncrementalCOOMatrix((num_users+num_users, num_movies+num_movies), np.int32)  # intializing to large initial state
    # initially ratings 1-5, 0 indicates no rating
    progress_step = int(num_movies*0.01)
    movies_count = 0
    file_num = 0
    for fl in ["combined_data_1.txt", "combined_data_2.txt", "combined_data_3.txt", "combined_data_4.txt"]:
        file_num += 1
        with open(path + '/' + fl, "r") as s:
            line = s.readline().strip()
            while line:
                if line.endswith(':'): #more efficient than ':' in afaik
                    movie_id = int(line.strip()[:-1])
                    movies_count += 1
                    #print('movie', movies_count)
                    if movies_count % progress_step == 0:
                        progress_handler(movies_count / num_movies * 100)
                else:
                    toks = line.split(",")
                    #print(toks)
                    nuid = int(toks[0])
                    rating = int(toks[1])
                    # TODO: For now, dropping dates, should we use another dimension for them?
                    #   toks[2]
                    iuid = idmap.create_or_get_iuid(nuid)

                    # https://maciejkula.github.io/2015/02/22/incremental-construction-of-sparse-matrices/
                    # movie_id-1 to ensure we use the first column
                    ratings.append(iuid, movie_id-1, rating)
                line = s.readline().strip()
    stop = time.time()
    print('time(minutes): ', (stop-start)/60)
    print(movies_count)
    print(len(idmap))
    return ratings, idmap
