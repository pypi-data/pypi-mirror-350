import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.feature_selection import SelectKBest, f_classif
from sklearn.linear_model import LogisticRegression


def prepare_features_target(df, features, target):
    X = df[features].values
    y = df[target].values
    return X, y


def split_train_test(X, y, test_size=0.2, random_state=None):
    return train_test_split(X, y, test_size=test_size, random_state=random_state)


def select_features(X_train, y_train, k=5):
    selector = SelectKBest(score_func=f_classif, k=k)
    X_new = selector.fit_transform(X_train, y_train)
    return X_new, selector

def train_model(X_train, y_train):
    model = LogisticRegression(max_iter=1000).fit(X_train, y_train)
    return model