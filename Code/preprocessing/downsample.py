from sklearn.model_selection import train_test_split


def reduce_movies_progress_handler(percentage):
    print('reducing movies:', percentage)


def reduce_movies(df, ratings_cutoff, progress_handler=reduce_movies_progress_handler):
    tmp = df[['movie_id', 'rating']].groupby('movie_id'). \
        count().rename(columns={'rating': 'count'}).sort_values('count')
    progress_handler(33)
    tmp = tmp[tmp['count'] > ratings_cutoff]
    progress_handler(66)
    return df[df.movie_id.isin(tmp.index)]


def reduce_users_progress_handler(percentage):
    print('reducing users:', percentage)


def reduce_users(df, ratings_cutoff, progress_handler=reduce_users_progress_handler):
    tmp = df[['user_id', 'rating']].groupby('user_id').\
        count().rename(columns={'rating': 'count'}).sort_values('count')
    progress_handler(33)
    tmp = tmp[tmp['count'] > ratings_cutoff]
    progress_handler(66)
    return df[df.user_id.isin(tmp.index)]


def reduce_SRSWR_progress_handler(percentage):
    print('SRSWR reducing:', percentage)


def reduce_SRSWR(df, random_state, progress_handler=reduce_SRSWR_progress_handler):
    _, small_sample_of_users = train_test_split(df['user_id'].unique(),
                                                test_size=0.005,
                                                random_state=random_state)
    progress_handler(50)
    return df[df['user_id'].isin(small_sample_of_users)]
