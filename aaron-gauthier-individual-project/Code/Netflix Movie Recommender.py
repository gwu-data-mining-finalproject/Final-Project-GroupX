import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import math
import seaborn as sns
import warnings
warnings.filterwarnings('ignore')

# Date not needed

netflix_df2 = pd.read_csv('few_samples_netflix.csv')

netflix_df2['rating'] = netflix_df2['rating'].astype(float)

print('Dataset 2 shape: {}'.format(netflix_df2.shape))
print('-Dataset examples-')
print(netflix_df2.iloc[::50000, :])

netflix_df2.head(5)

netflix_movie_titles_df5 = pd.read_csv('movie_titles.txt', delimiter='\t', header=None)
#netflix_movie_titles_df5.drop(['Unnamed: 3', 'Unnamed: 4', 'Unnamed: 5'], axis =1)
netflix_movie_titles_df5 = netflix_movie_titles_df5.iloc[:, 0:3]
netflix_movie_titles_df5.columns = ['movie_id', 'year', 'movie_title']
netflix_movie_titles_df5['year'] = netflix_movie_titles_df5['year']
netflix_movie_titles_df5.head(5)

full_netflix_data = pd.merge(netflix_df2, netflix_movie_titles_df5, on='movie_id')
full_netflix_data.head(5)

# Lets see what we have here
full_netflix_data.describe()['rating']

print("Number of NaN values in Netflix dataframe : ", sum(full_netflix_data.isnull().any()))

duplicates = full_netflix_data.duplicated(['movie_id','user_id','rating'])
dups = sum(duplicates) # by considering all columns..( including timestamp)
print("There are {} duplicate rating entries in the data.".format(dups))

print("Total data ")
print("-"*50)
print("\nTotal number of ratings :",full_netflix_data.shape[0])
print("Total number of users   :", len(np.unique(full_netflix_data.user_id)))
print("Total number of movies  :", len(np.unique(full_netflix_data.movie_id)))

print('Full Netflix dataset shape: {}'.format(full_netflix_data.shape))
print('---Dataset examples---')
print(full_netflix_data.iloc[::50000, :])

full_netflix_data.head(5)

# play with quartile because it may affect model accuracy

count_mean_vars = ['count', 'mean']

movie_summary_df = full_netflix_data.groupby('movie_id')['rating'].agg(count_mean_vars)
movie_summary_df.index = movie_summary_df.index.map(int)
movie_benchmark = round(movie_summary_df['count'].quantile(0.70), 0)
movie_list_benchmark_drop = movie_summary_df[movie_summary_df['count'] < movie_benchmark].index

print('Minimum number of times movies were reviewed: {}'.format(movie_benchmark))

customer_summary_df = full_netflix_data.groupby('user_id')['rating'].agg(count_mean_vars)
customer_summary_df.index = customer_summary_df.index.map(int)
customer_benchmark = round(customer_summary_df['count'].quantile(0.70), 0)
customer_list_benchmark_drop = customer_summary_df[customer_summary_df['count'] < customer_benchmark].index

print('Minimum number of times customers reviewed movies: {}'.format(customer_benchmark))

#clean up NaN's
full_netflix_data_dummy = full_netflix_data.copy().fillna(0)

full_netflix_data_dummy.head(10)


export_csv_netflix_full_movie = full_netflix_data_dummy.to_csv (r'C:\Users\AaronDataScienceComp\Documents\export_data_netflix_full_movies.csv', index = None, header=True)

export_csv_netflix_full_movie

full_netflix_data_dummy.groupby('movie_title')['rating'].mean().sort_values(ascending=False).head()

# Export to CSV file Netflix Rating mean
export_csv_netflix_rating_mean = netflix_rating_mean.to_csv (r'C:\Users\AaronDataScienceComp\Documents\export_data_netflix_rating_mean.csv', index = None, header=True)

export_csv_netflix_rating_mean

# Output dataframe with movie_title, rating and number_ratings (total ratings count per movie)

full_netflix_data_dummy.groupby('movie_title')['rating'].count().sort_values(ascending=False).head()

movie_rating_counts = pd.DataFrame(full_netflix_data_dummy.groupby('movie_title')['rating'].mean())

movie_rating_counts['number_ratings'] = pd.DataFrame(full_netflix_data_dummy.groupby('movie_title')['rating'].count())

movie_rating_counts.head(5)

# More graphs to visualize data

import matplotlib.pyplot as plt
import seaborn as sns

sns.set_style('white')
%matplotlib inline

# Graph of ratings column

plt.figure(figsize =(10,4))

movie_rating_counts['number_ratings'].hist(bins = 10)

# plot graph of ratings column
plt.figure(figsize = (10,4))

movie_rating_counts['rating'].hist(bins = 100)

# method to make y-axis more readable
def human(num, units = 'M'):
    units = units.lower()
    num = float(num)
    if units == 'k':
        return str(num/10**3) + " K"
    elif units == 'm':
        return str(num/10**6) + " M"
    elif units == 'b':
        return str(num/10**9) +  " B"



fig, ax = plt.subplots()
plt.title('Distribution of ratings over full Netflix dataset', fontsize=15)
sns.countplot(full_netflix_data.rating)
ax.set_yticklabels([human(item, 'M') for item in ax.get_yticks()])
ax.set_ylabel('Number of Ratings (Millions)')

plt.show()


# user_id groupby to rating
rated_movies_per_user = full_netflix_data.groupby(by='user_id')['rating'].count().sort_values(ascending=False)

rated_movies_per_user.head()

# How do we best mathematically describe (and visually display) random variables?
# The answer is we use probability density functions (PDF) and cumulative density functions (CDF).
# CDFs are simpler to comprehend for both discrete and continuous random variables than PDFs.

fig = plt.figure(figsize=plt.figaspect(.5))

ax1 = plt.subplot(121)
sns.kdeplot(rated_movies_per_user, shade=True, ax=ax1)
plt.xlabel('Ratings by user')
plt.title("Probability Density Function (PDF)")

ax2 = plt.subplot(122)
sns.kdeplot(rated_movies_per_user, shade=True, cumulative=True,ax=ax2)
plt.xlabel('Ratings by user')
plt.title('Cumulative Density Function (CDF)')

plt.show()

rated_movies_per_user.describe()

quantiles = rated_movies_per_user.quantile(np.arange(0,1.01,0.01), interpolation='higher')

plt.title("Full Netflix Dataset Quantiles and Values")
quantiles.plot()
# quantiles with 0.05 difference
plt.scatter(x=quantiles.index[::5], y=quantiles.values[::5], c='orange', label="quantiles with 0.05 intervals")
# quantiles with 0.25 difference
plt.scatter(x=quantiles.index[::25], y=quantiles.values[::25], c='m', label = "quantiles with 0.25 intervals")
plt.ylabel('Ratings by user')
plt.xlabel('Value at quantile')
plt.legend(loc='best')

# annotate the 25th, 50th, 75th and 100th percentile values....
for x,y in zip(quantiles.index[::25], quantiles[::25]):
    plt.annotate(s="({} , {})".format(x,y), xy=(x,y), xytext=(x-0.05, y+500)
                ,fontweight='bold')


plt.show()

quantiles[::5]

print('\n Ratings at last 5 percentile : {}\n'.format(sum(rated_movies_per_user>= 923)))

ratings_per_movie = full_netflix_data.groupby(by='movie_id')['rating'].count().sort_values(ascending=False)

fig = plt.figure(figsize=plt.figaspect(.5))
ax = plt.gca()
plt.plot(ratings_per_movie.values)
plt.title('Ratings per movie')
plt.xlabel('Movie')
plt.ylabel('Users who rated a movie')
ax.set_xticklabels([])

plt.show()

#sort values based on the number of rating column

movie_piv = full_netflix_data_dummy.pivot_table(index = 'user_id', columns = 'movie_title', values = 'rating')

movie_piv.head(5)

movie_rating_counts.sort_values('number_ratings', ascending = False).head(5)

# Analysing correlation with similar movies
misscongeniality_user_ratings = movie_piv['Miss Congeniality']
thegodfather_user_ratings = movie_piv['The Godfather']

misscongeniality_user_ratings.head()

thegodfather_user_ratings.head()

# Analyzing the correlation with similar movies
similar_to_misscongeniality = movie_piv.corrwith(misscongeniality_user_ratings)

corr_misscongeniality = pd.DataFrame(similar_to_misscongeniality, columns = ['Correlation'])
corr_misscongeniality.dropna(inplace = True)
corr_misscongeniality.head(10)


# Similar movies like Miss Congeniality
corr_misscongeniality.sort_values('Correlation', ascending = False).head(10)
corr_misscongeniality = corr_misscongeniality.join(movie_rating_counts['number_ratings'])
corr_misscongeniality.head()
corr_misscongeniality[corr_misscongeniality['number_ratings']>100].sort_values('Correlation', ascending = False).head()


# Analyzing the correlation with similar movies
similar_to_thegodfather = movie_piv.corrwith(thegodfather_user_ratings)

corr_thegodfather = pd.DataFrame(similar_to_thegodfather, columns = ['Correlation'])
corr_thegodfather.dropna(inplace = True)
corr_thegodfather.head(10)


# Similar movies like Miss Congeniality
corr_thegodfather.sort_values('Correlation', ascending = False).head(10)
corr_thegodfather = corr_thegodfather.join(movie_rating_counts['number_ratings'])
corr_thegodfather.head()
corr_thegodfather[corr_thegodfather['number_ratings']>100].sort_values('Correlation', ascending = False).head()










































































