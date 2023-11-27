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
        unique_scores = (self.df[col].nunique() / len(self.df[col]) for col in self.df.columns)
        return np.average(list(unique_scores), weights=list(self.weights.values()))

    def consistency(self):
        consistency_scores = []
        for col in self.df.columns:
            most_common_type = self.df[col].map(type).mode()[0]
            consistency = (self.df[col].map(type) == most_common_type).mean()
            consistency_scores.append(consistency)
        return np.average(consistency_scores, weights=list(self.weights.values()))


    def readability(self, column):
        if column in self.df.columns and self.df[column].dtype == 'object':
            vectorizer = TfidfVectorizer()
            tfidf_matrix = vectorizer.fit_transform(self.df[column].astype(str))
            cosine_sim = cosine_similarity(tfidf_matrix)
            return np.mean(cosine_sim.diagonal())
        return 1
