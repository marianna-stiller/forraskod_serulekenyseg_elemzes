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
from sklearn.ensemble import RandomForestClassifier
from sklearn.neighbors import KNeighborsClassifier
from sklearn.linear_model import LogisticRegression
from sklearn.calibration import CalibratedClassifierCV
from sklearn.svm import LinearSVC

develop = False
gnb_pr_ar = []
rfc = RandomForestClassifier()
rfc_pr_ar = []
nknc = KNeighborsClassifier()
nknc_pr_ar = []
lr = LogisticRegression(solver='lbfgs', max_iter=10000, multi_class='ovr')
lr_pr_ar = []
lsvc = CalibratedClassifierCV(LinearSVC(max_iter=10000, multi_class='ovr'))
lsvc_pr_ar = []

def main(argv=None):
    if argv is None:
        argv = sys.argv

    origX = np.load("testX.npy")
    origY = np.load("testy.npy").astype(int)
    origX2 = np.load("toimportX.npy")
    origY2 = np.load("toimporty.npy").astype(int)

    kFold = RepeatedStratifiedKFold(n_splits=5, n_repeats=5)

    for train_index, test_index in kFold.split(origX, origY):
        trainX, testX = origX[train_index], origX[test_index]
        trainY, testY = origY[train_index], origY[test_index]

        # Naive Bayes: Gaussian
        Classifier = classifier(trainX, trainY)
        results = test_bmodel(testX, testY, Classifier)
        gnb_pr_ar.append(results)
        # Ensemble Method: Random Forest
        rfc.fit(trainX, trainY)
        rfc_pr_ar.append(test_bmodel(testX, testY, rfc))
        # Nearest Neighbors: K-Nearest Neighbors
        nknc.fit(trainX, trainY)
        nknc_pr_ar.append(test_bmodel(testX, testY, nknc))
        # Linear Model: Logistic Regression
        lr.fit(trainX, trainY)
        lr_pr_ar.append(test_bmodel(testX, testY, lr))
        # Support Vector Machine: LinearSVC
        lsvc.fit(trainX, trainY)
        lsvc_pr_ar.append(test_bmodel(testX, testY, lsvc))

    classifier2(origX2,origY2)
    print("Gaussian Naive Bayes precision:", average(gnb_pr_ar))
    print("Random Forest preicison:", average(rfc_pr_ar))
    print("K-Nearest Neighbors precision:", average(nknc_pr_ar))
    print("Logistic Regression precision:", average(lr_pr_ar))
    print("LinearSVC precision:", average(lsvc_pr_ar))


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