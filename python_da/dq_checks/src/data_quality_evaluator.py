from datetime import datetime
import re
import pandas as pd
import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity


class AdvancedDataQualityEvaluator:
    def __init__(self, dataframe, weights=None, preprocessing_complexity=None):
        self.df = dataframe
        self.weights = weights or self.default_weights()
        self.preprocessing_complexity = preprocessing_complexity or 1

    def default_weights(self):
        weights = {}
        for col in self.df.columns:
            if self.df[col].dtype == 'object':
                weights[col] = 1.5
            else:
                weights[col] = 1
        return weights

    def completeness(self):
        completeness_scores = (self.df[col].notnull().mean() for col in self.df.columns)
        return np.average(list(completeness_scores), weights=list(self.weights.values()))

    def uniqueness(self):
        
        text_columns = [col for col in self.df.columns if self.df[col].dtype == 'object']

        # Calculate uniqueness score for each text column low means good
        # Inverse of previous
        unique_scores = [(len(self.df[col]) - self.df[col].nunique()) / len(self.df[col]) for col in text_columns]

        # Calculate the average uniqueness score else give 1 if no text columns
        return np.mean(unique_scores) if unique_scores else 1


    def consistency(self):
        consistency_scores = []
        for col in self.df.columns:
            most_common_type = self.df[col].map(type).mode()[0]
            consistency = (self.df[col].map(type) == most_common_type).mean()
            consistency_scores.append(consistency)
        return np.average(consistency_scores, weights=list(self.weights.values()))


    def readability(self, column, sample_size=100):
        if column in self.df.columns and self.df[column].dtype == 'object':
            # Use a smaller sample if the dataframe is large
            if len(self.df) > sample_size:
                sample_df = self.df[column].sample(n=sample_size, random_state=1).astype(str)
            else:
                sample_df = self.df[column].astype(str)

            vectorizer = TfidfVectorizer()
            tfidf_matrix = vectorizer.fit_transform(sample_df)
            cosine_sim = cosine_similarity(tfidf_matrix)
            return np.mean(cosine_sim.diagonal())

        return 1
