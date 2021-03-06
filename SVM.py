#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Apr 14 13:11:51 2018

@author: parth
"""

import pandas as pd
from sklearn import svm
from sklearn.model_selection import StratifiedShuffleSplit
from sklearn.metrics import classification_report
from sklearn.metrics import average_precision_score
from sklearn.metrics import precision_recall_curve
import matplotlib.pyplot as plt
import time


def normalize(X):
    
    for feature in X.columns:
        X[feature] -= X[feature].mean()
        X[feature] /= X[feature].std()
        
    return X


def undetectedFraudRate(test, pred):
    
    det = 0
    fraud = 0
    predF = 0
    
    for i in range(0, len(test)):
        if(pred[i]==1):
            predF = predF + 1
        
        if(test[i]==1):
            fraud = fraud + 1
            if(pred[i]==1):
                det = det + 1
                
    return det, fraud, predF


if __name__ == "__main__":
    
    st_time = time.time()
    pd.options.mode.chained_assignment = None
    
    data = pd.read_csv('../creditcard.csv')
    
    features = ['Amount'] + ['V%d' % number for number in range (1,29)]
    target = 'Class'
    
    X = data[features]
    Y = data[target]
    
    splitter = StratifiedShuffleSplit(n_splits=1, test_size=0.4, random_state=0)
    
    model = svm.SVC(kernel='rbf', C=1, gamma=10)
    
    for train_indices, test_indices in splitter.split(X,Y):
        
        X_train, Y_train = X.iloc[train_indices], Y.iloc[train_indices]
        X_test, Y_test = X.iloc[test_indices], Y.iloc[test_indices]
        
        X_train = normalize(X_train)
        X_test = normalize(X_test)
        
        model.fit(X_train, Y_train)
        predicted = model.predict(X_test)
        
        print('\nClassification report: \n{}'.format(classification_report(Y_test, predicted)))
        
        det, tot1, tot2 = undetectedFraudRate(Y_test.values, predicted)
        print('Precision:\t{} %\nRecall:\t\t{} %'.format(det/tot2*100,det/tot1*100))
        
        avg_precision = average_precision_score(Y_test, predicted)
        
        precision, recall, _ = precision_recall_curve(Y_test, predicted)
        plt.step(recall, precision, color='r', alpha=0.2, where='post')
        plt.fill_between(recall, precision, step='post', alpha=0.2, color='r')
        plt.xlabel('Recall')
        plt.ylabel('Precision')
        plt.xlim([0.0, 1.05])
        plt.ylim([0.0, 1.0])
        plt.title('Fraud detection precision-recall curve: AP = {}'.format(avg_precision))
        
    print('\nExecution time: {} seconds'.format(time.time()-st_time))