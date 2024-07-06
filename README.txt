In this project I have used the Movielens 100k dataset to create a Movie Recommendation System in Python. (I am also beginning to create a website where the system functions)

Each user in this dataset has rated 20 movies out of the 1682 movies available on the dataset.

For this I have only used cosine similarity in order to determine the similarities in each user's ratings of the movies they have watched. Within the dataset, each user's age, gender (Male or Female), and occupation has been recorded also.
Using all of this data, I have been able to complete a recommendation system that recommends movies from the dataset based on the ratings given from each user, their ages, genders and occupations.

For the user ratings , I only did cosine similarity to convert the differences of each users ratings compared to each other into one value for every two users comparison, showing 1.00 for complete similarity which only occured when a user was compared with themselves.
However, for each user's demographic information I had to go down a different route. Although age was a numerical value that cosine similarity could be performed on, gender and occupation were not. 

To fix this I used pd.getdummies to display the different occupations in binary, manually represented the genders in binary format and then imported the euclidean_distances function. 
Once everything was done I had two sets of data (user_ratings and user_demographics) which i combined after normalising and weighting each of them. Using the weights allowed me to control the influence of each dataset on the final combined similarity score.
I created a function to get the recommendations and then I was done.

Now I have begun to design a website using HTML and CSS. I am also using flask as a means to use the python code I have written in the website. 
