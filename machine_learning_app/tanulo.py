"""
This file implements the real learning.
"""

import sys
import numpy as np
import itertools
import matplotlib.pyplot as plt
import pickle
from matplotlib import cm
from keras.utils import to_categorical
from sklearn.naive_bayes import MultinomialNB, GaussianNB, BernoulliNB
from sklearn import svm
from sklearn.calibration import CalibratedClassifierCV
from sklearn.ensemble import GradientBoostingClassifier, ExtraTreesClassifier
from sklearn.tree import DecisionTreeClassifier, ExtraTreeClassifier
from sklearn.neighbors import KNeighborsClassifier
from sklearn.linear_model import LogisticRegression
from sklearn.datasets import load_iris

from sklearn import datasets
from sklearn.model_selection import RepeatedStratifiedKFold
from sklearn.model_selection import train_test_split
from sklearn.neural_network import MLPClassifier
from sklearn.semi_supervised import LabelSpreading, LabelPropagation
from sklearn.metrics import precision_recall_fscore_support
from sklearn.metrics import accuracy_score
from sklearn.metrics import confusion_matrix

develop = False

def main(argv=None):
    if argv is None:
        argv = sys.argv

    origX = np.load("testX.npy")
    origY = np.load("testy.npy").astype(int)
    origX2 = np.load("toimportX.npy")
    origY2 = np.load("toimporty.npy").astype(int)

    kFold = RepeatedStratifiedKFold(n_splits=5, n_repeats=5)

    for train_index, validation_index in kFold.split(origX, origY):
        trainX, validationX = origX[train_index], origX[validation_index]
        trainY, validationY = origY[train_index], origY[validation_index]

        Classifier = classifier(trainX, trainY)

        results = test_bmodel(validationX, validationY, Classifier)
        #print(results)

    classifier2(origX2,origY2)

def classifier2(X, Y):
    myClassifier2 = pickle.loads(s)

    predict1 = myClassifier2.predict_proba(X)
    predict2 = myClassifier2.predict(X)

    print(predict1.item(0))
    print(predict1.item(1))
    #print(predict1)
    #print(predict2)

def classifier(X, Y):
    global s
    """Linear SVM

       Parameters:
       -----------
       X           : array like test samples [n sample, m features]
       Y           : n element array like vector containing real labels

       Returns the trained classifier.
    """
    # 1
    myClassifier = ExtraTreesClassifier()
    # 2
    # myClassifier = GaussianNB()
    # 3
    # myClassifier = GradientBoostingClassifier()
    # 4
    # myClassifier = DecisionTreeClassifier()
    # 5
    # myClassifier = KNeighborsClassifier()
    # 6
    # myClassifier = LogisticRegression(multi_class='ovr')
    # 7
    #mySVM = svm.LinearSVC(multi_class='ovr')
    #myClassifier = CalibratedClassifierCV(mySVM)

    # myClassifier = CalibratedClassifierCV(myLog)
    # myClassifier = MultinomialNB()
    # myClassifier = BernoulliNB()
    # myClassifier = GaussianProcessClassifier(multi_class='one_vs_rest')
    # myClassifier = ExtraTreeClassifier()
    # myClassifier = LabelSpreading()
    # myClassifier = LabelPropagation()
    # myClassifier = MLPClassifier(hidden_layer_sizes=25, max_iter=50, early_stopping=True)
    
    myClassifier.fit(X, Y)
    # Save the trained model as a pickle string
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

    evaluation = precision_recall_fscore_support(Y, Y_pred, pos_label=1, average='micro')

    return evaluation

if __name__ == "__main__":
    sys.exit(main())