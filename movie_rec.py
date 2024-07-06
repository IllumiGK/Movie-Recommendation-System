from flask import Flask, request, render_template
import pandas as pd
from sklearn.metrics.pairwise import cosine_similarity
import numpy as np
from sklearn.metrics import mean_squared_error
from collections import Counter
from sklearn.metrics.pairwise import euclidean_distances

app = Flask(__name__, static_url_path='/static', static_folder='static')

def get_recommendations(user_id, num_recommendations=5):
    # Finds the movies the most similar users to 'user_id' rated and adds them to recommendation table (excluding those that werent rated by the users), groups them alphabetically and sorts them from most highly rated to least and then returns the sorted table.
    similar_users = user_similarity_df[user_id].sort_values(ascending=False).index[1:num_recommendations+1]
    recommendations = pd.Series()
    similarity_sum = 0
    for user in similar_users:
        similarity_score = user_similarity_df[user_id][user]
        watched_movies = user_item_matrix.loc[user] * similarity_score
        
        recommendations = recommendations.append(watched_movies[watched_movies > 0])
        similarity_sum += similarity_score
    # !!!![Along with user similarity, figure out a way to include age, gender, and occupation trends for each film when figuring out the user recommendations...]
    recommendations = recommendations.groupby(recommendations.index).sum()
    if similarity_sum > 0:
        recommendations /= similarity_sum
    
    recommendations = recommendations.sort_values(ascending=False)
    return recommendations.head(num_recommendations)
def get_recommendations_with_demographics(user_id, num_recommendations=5):
    # Finds the movies the most similar users to 'user_id' rated and adds them to recommendation table (excluding those that werent rated by the users), groups them alphabetically and sorts them from most highly rated to least and then returns the sorted table.
    similar_users = combined_similarity_df[user_id].sort_values(ascending=False).index[1:num_recommendations+1]
    recommendations = pd.Series(dtype=float)
    similarity_sum = 0
    for user in similar_users:
        similarity_score = combined_similarity_df[user_id][user]
        watched_movies = user_item_matrix.loc[user] * similarity_score
        
        recommendations = recommendations._append(watched_movies[watched_movies > 0])
        similarity_sum += similarity_score
    # [Along with user similarity, figure out a way to include age, gender, and occupation trends for each film when figuring out the user recommendations...] ------- NOW COMPLETED!
    recommendations = recommendations.groupby(recommendations.index).sum()
    if similarity_sum > 0:
        recommendations /= similarity_sum
    
    recommendations = recommendations.sort_values(ascending=False)
    return recommendations.head(num_recommendations)

@app.route('/recommend', methods=['GET', 'POST'])
def recommend():
    if request.method == 'POST':
        try:
            user_id = int(request.form['user_id'])
            recommendations = get_recommendations_with_demographics(user_id)
            return render_template('index.html', recommendations=recommendations)
        except Exception as e:
            app.logger.error(f"Error: {e}")
            return render_template('index.html', recommendations=None)
    elif request.method == 'GET':
        return render_template('index.html', recommendations=None)


@app.route('/')
def home():
    return render_template('home.html', recommendations = None)

# Get all info for all the similar users and put them into sorted lists
def get_similar_users_info(user_id):
    similar_users1 = user_similarity_df[user_id].sort_values(ascending=False).index[0:10]
    occupation = []
    gender = []
    
    age = []
    for j in similar_users1:
        info = []       
        for i in user_info.loc[j]:
            info.append(str(i))

        a,b,c = info
        age.append(a)
        gender.append(b)
        occupation.append(c)
        

    # Look for the most common attributes of all the similar users to determine any trends/patterns

    wc = Counter(occupation)
    s = max(wc.values())
     
    print(wc.items())

def rmse(pred, actual):
    return np.sqrt(mean_squared_error(pred, actual))



# user_id = int(input('Enter your UserID number: '))

ratings_column_names = ['user_id', 'item_id', 'rating', 'timestamp']

# Established two dataframes - Ratings and Movie_titles
ratings = pd.read_csv('C:\\Users\\illum\\VSCode\\Project_1\\ml-100k\\u.data', sep='\t', names=ratings_column_names)
movie_titles = pd.read_csv('C:\\Users\\illum\\VSCode\\Project_1\\ml-100k\\u.item', sep='|', encoding='latin-1', header=None, usecols=[0, 1])
movie_titles.columns = ['item_id', 'title']

# Merged the two dataframes into one using 'item_id' as the foreign key
data = pd.merge(ratings, movie_titles, on='item_id' )

# Organised the merged dataframes into a pivot table with the titles of the movies representing each column, the 'user_id' as the index and the ratings given as the values inside the table under every column
user_item_matrix = data.pivot_table(index='user_id', columns='title', values='rating')

# Filled all null values where a user didnt rate that movie with 0s
user_item_matrix.fillna(0, inplace=True)

# Found similarities in ratings between users using cosine similarity and put it into a dataframe
user_similarity = cosine_similarity(user_item_matrix)
user_similarity_df = pd.DataFrame(user_similarity, index=user_item_matrix.index, columns=user_item_matrix.index)

# Get data from u.user and put into dataframe
info_column_names = ['user_id', 'age', 'gender', 'occupation', 'zipcode']
user_info = pd.read_csv('C:\\Users\\illum\\VSCode\\Project_1\\ml-100k\\u.user', sep='|', names=info_column_names )
user_info = user_info.drop(columns='zipcode')


# Convert categorical variables into numerical representations
user_info['gender'] = user_info['gender'].map({'M': 0, 'F': 1})
user_info = pd.concat([user_info, pd.get_dummies(user_info['occupation'], prefix='occ')], axis=1).drop(columns=['occupation'])

# Calculate euclidean distances between users based on demographic info
demographic_features = user_info.drop(columns=['user_id'])
demographic_similarity = 1 / (1 + euclidean_distances(demographic_features))
demographic_similarity_df = pd.DataFrame(demographic_similarity, index=user_info['user_id'], columns=user_info['user_id'])

# Normalise both matrices to have values between 0 and 1

demographic_similarity_normalised = (demographic_similarity - demographic_similarity.min())/(demographic_similarity.max()-demographic_similarity.min())
ratings_similarity_normalised = (user_similarity - user_similarity.min())/(user_similarity.max() - user_similarity.min())

# Combine the similarities with weighted sum 
alpha = 0.7
beta = 0.3

combined_similarity = alpha * ratings_similarity_normalised + beta * demographic_similarity_normalised
combined_similarity_df = pd.DataFrame(combined_similarity, index=user_item_matrix.index, columns=user_item_matrix.index)

# Print results
#recommendations = get_recommendations_with_demographics(user_id)
#print(f"Recommendations for User {user_id} including demographics:\n{recommendations}")
#recommendations = get_recommendations(user_id)
#print(f"Recommendations for User {user_id} not including demographics:\n{recommendations}")



if __name__ == '__main__':
    app.run(debug=True)