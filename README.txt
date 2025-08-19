Movie Recommendation System
📌 Executive Summary

This project demonstrates a hybrid movie recommendation system built with the Movielens 100k dataset, combining both user ratings and demographic information (age, gender, occupation) to improve recommendation accuracy. It applies cosine similarity for collaborative filtering, Euclidean distance for demographic features, and a weighted hybrid approach to generate personalized recommendations. The model achieves RMSE: 1.042 and MAE: 0.835, and is currently being integrated into a Flask web app with a custom frontend.

Dataset

The Movielens 100k dataset contains 1,682 movies and user ratings, with each user rating 20 movies. Demographic information recorded includes age, gender, and occupation.

Methodology

User Ratings

Cosine similarity was applied to compare users’ ratings of movies.

A similarity score of 1.0 indicates identical ratings (only occurs when comparing a user to themselves).

User Demographics

Age was used as a numerical feature with cosine similarity.

Gender and occupation were encoded as binary features using pd.get_dummies and manual encoding.

Euclidean distance was applied to the demographic features.

Hybrid Model

The ratings and demographics similarities were normalized and weighted to produce a final combined similarity score.

Weighting allows control over how much influence each dataset has on the recommendations.

Recommendation Function

Two functions were created:

Without demographics — recommendations based solely on ratings.

With demographics — recommendations using the hybrid weighted score.

This allows easy comparison of the impact of demographic information on recommendation quality.

Results

RMSE: 1.042

MAE: 0.835

The evaluation shows the hybrid model performs well on this dataset and demonstrates the potential improvement from incorporating demographic features.

Web Integration

Currently developing a Flask web app using HTML and CSS to allow users to input ratings and receive recommendations directly from the web interface.

Future Work

Complete the web app frontend for full user interactivity.

Experiment with additional weighting strategies or alternative similarity metrics.

Scale the model to larger datasets for improved generalization.
