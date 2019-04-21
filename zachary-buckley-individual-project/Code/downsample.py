from sklearn.model_selection import train_test_split


def reduce_movies_progress_handler(percentage):
    """
    Function for printing out progress information
    :param percentage: progress percentage
    """
    print('reducing movies:', percentage)


def reduce_movies(df, ratings_cutoff, progress_handler=reduce_movies_progress_handler):
    """
    Function responsible for reduce number of movies by filtering based on ratings_cutoff
    :param df: dataframe to be reduced
    :param ratings_cutoff: minimum number of ratings for a movie to stay in the df
    :param progress_handler: function for handling incremental progress reporting
    :return: dataframe that has been further reduced.
    """
    tmp = df[['movie_id', 'rating']].groupby('movie_id'). \
        count().rename(columns={'rating': 'count'}).sort_values('count')
    progress_handler(33)
    tmp = tmp[tmp['count'] > ratings_cutoff]
    progress_handler(66)
    return df[df.movie_id.isin(tmp.index)]


def reduce_users_progress_handler(percentage):
    """
    Function for printing out progress information
    :param percentage: progress percentage
    """
    print('reducing users:', percentage)


def reduce_users(df, ratings_cutoff, progress_handler=reduce_users_progress_handler):
    """
    Function  responsible for reducing the dataset based on users rating count
    :param df: dataframe to be reduced
    :param ratings_cutoff: minimum number of ratings a user needs to have to be included in reduced dataset
    :param progress_handler: function for handling incremental progress reporting
    :return: dataframe that has been further reduced.
    """
    tmp = df[['user_id', 'rating']].groupby('user_id').\
        count().rename(columns={'rating': 'count'}).sort_values('count')
    progress_handler(33)
    tmp = tmp[tmp['count'] > ratings_cutoff]
    progress_handler(66)
    return df[df.user_id.isin(tmp.index)]


def reduce_SRSWR_progress_handler(percentage):
    """
    Function for printing out progress information
    :param percentage: progress percentage
    """
    print('SRSWR reducing:', percentage)


def reduce_SRSWR(df, random_state, progress_handler=reduce_SRSWR_progress_handler):
    """
    Function responsible for performing SRSOR against the users in the dataset
    Note: original name for the function was SRSWR, and refactoring was a bit too time consuming
    to make sense, but indeed the function is actually performing SRSOR (simple random sample without replacement)
    :param df: dataframe to be reduced
    :param random_state: random state value to be used by sklearn's train_test_split
    :param progress_handler: function for handling incremental progress
    :return: dataframe that has been reduced by SRSOR
    """
    _, small_sample_of_users = train_test_split(df['user_id'].unique(),
                                                test_size=0.005,
                                                random_state=random_state)
    progress_handler(50)
    return df[df['user_id'].isin(small_sample_of_users)]
