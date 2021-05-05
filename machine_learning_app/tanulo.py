"""
Spyder Editor

This is a temporary script file.
"""

import sys
import numpy as np
import itertools
import matplotlib.pyplot as plt
import pickle
from matplotlib import cm
from keras.utils import to_categorical
from sklearn import svm
from sklearn.model_selection import RepeatedStratifiedKFold
from sklearn.metrics import precision_recall_fscore_support
from sklearn.metrics import accuracy_score
from sklearn.metrics import confusion_matrix

from sklearn.naive_bayes import GaussianNB
from sklearn.ensemble import ExtraTreesClassifier
from sklearn.tree import DecisionTreeClassifier
from sklearn.neighbors import KNeighborsClassifier
from sklearn.ensemble import RandomForestClassifier


develop = False

def main(argv=None):
    if argv is None:
        argv = sys.argv

    gnb_pr_ar = []
    etc = ExtraTreesClassifier()
    etc_pr_ar = []
    dtc = DecisionTreeClassifier()
    dtc_pr_ar = []
    nknc = KNeighborsClassifier()
    nknc_pr_ar = []

    origX = np.load("testX.npy")
    origY = np.load("testy.npy").astype(int)
    origX2 = np.load("toimportX.npy")
    origY2 = np.load("toimporty.npy").astype(int)

    kFold = RepeatedStratifiedKFold(n_splits=5, n_repeats=5)

    for train_index, validation_index in kFold.split(origX, origY):
        trainX, validationX = origX[train_index], origX[validation_index]
        trainY, validationY = origY[train_index], origY[validation_index]
        
        # Gaussian Naive Bayes
        Classifier = classifier(trainX, trainY)
        results = test_bmodel(validationX, validationY, Classifier)
        gnb_pr_ar.append(results)
        # Extra Trees
        etc.fit(trainX, trainY)
        etc_pr_ar.append(test_bmodel(validationX, validationY, etc))
        # Decision Tree
        dtc.fit(trainX, trainY)
        dtc_pr_ar.append(test_bmodel(validationX, validationY, dtc))
        # KNeighbors
        nknc.fit(trainX, trainY)
        nknc_pr_ar.append(test_bmodel(validationX, validationY, nknc))

    classifier2(origX2,origY2)
    print("Gaussian precision:",average(gnb_pr_ar))
    print("Extra Trees preicison:",average(etc_pr_ar))
    print("Decision Tree precision:",average(dtc_pr_ar))
    print("KNeighbors precision:",average(nknc_pr_ar))


def average(lst):
    return sum(lst) / len(lst)

def classifier2(X, Y):
    myClassifier2 = pickle.loads(s)

    predict = myClassifier2.predict_proba(X)
    print(predict.item(0))
    print(predict.item(1))
    print(myClassifier2.predict(X))


def classifier(X, Y):
    global s
    """Linear SVM

       Parameters:
       -----------
       X           : array like test samples [n sample, m features]
       Y           : n element array like vector containing real labels

       Returns the trained classifier.
    """
    myClassifier = GaussianNB()
    myClassifier.fit(X, Y)
    s = pickle.dumps(myClassifier)
    return myClassifier


def test_bmodel(X, Y, classifier):
    """This method tests a classifier using validation data.

        Parameters:
        -----------
        X           : array like test samples [n sample, m features]
        Y           : n element array like vector containing real labels
        classifier  : a list of binary classifiers to be tested
       
        This function returns a dictionary containing labels and the
        corresponding metrics (precision, recall, Fscore and support).
    """

    Y_pred = np.argmax(classifier.predict_proba(X), axis=1)

    precision, recall, fscore, support = precision_recall_fscore_support(Y, Y_pred, pos_label=1, average='micro')

    return recall


if __name__ == "__main__":
    sys.exit(main())