#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Apr 13 00:13:26 2018

@author: parth
"""

import pandas as pd
from sklearn.model_selection import StratifiedShuffleSplit
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import classification_report


def normalize(X):
    
    for feature in X.columns:
        X[feature] -= X[feature].mean()
        X[feature] /= X[feature].std()
        
    return X


if __name__ == "__main__":
    data = pd.read_csv('creditcard.csv')
    
    features = ['Amount'] + ['V%d' % number for number in range (1,29)]
    target = 'Class'
    
    X = data[features]
    Y = data[target]
        
    model = LogisticRegression()
    splitter = StratifiedShuffleSplit(n_splits=1, test_size=0.5, random_state=0)
    
    for train_indices, test_indices in splitter.split(X,Y):
        
        X_train, Y_train = X.iloc[train_indices], Y.iloc[train_indices]
        X_test, Y_test = X.iloc[test_indices], Y.iloc[test_indices]
        
        X.train = normalize(X_train)
        X.test = normalize(X_test)
        
        model.fit(X_train, Y_train)
        predicted = model.predict(X_test)
        
        print(classification_report(Y_test, predicted))