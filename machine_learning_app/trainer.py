"""
Spyder Editor

This is a temporary script file.
"""

import sys
import json
import numpy as np
import itertools
import matplotlib.pyplot as plt
import pickle
from prettytable import PrettyTable
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

gnb = GaussianNB()
gnb_pr_ar = []
rfc = RandomForestClassifier()
rfc_pr_ar = []
nknc = KNeighborsClassifier()
nknc_pr_ar = []
lr = LogisticRegression(solver='lbfgs', max_iter=10000, multi_class='ovr')
lr_pr_ar = []
lsvc = CalibratedClassifierCV(LinearSVC(max_iter=10000, multi_class='ovr'))
lsvc_pr_ar = []

def main(p1, p2, p3):
    origX = np.load(p1)
    origY = np.load(p2).astype(int)
    origX2 = np.load(p3)

    kFold = RepeatedStratifiedKFold(n_splits=5, n_repeats=5)
    i = 0
    for train_index, test_index in kFold.split(origX, origY):
        trainX, testX = origX[train_index], origX[test_index]
        trainY, testY = origY[train_index], origY[test_index]

        # Naive Bayes: Gaussian
        recall_gnb_i = classifier(trainX, trainY, testX, testY, gnb, i)
        gnb_pr_ar.append(recall_gnb_i)
        # Ensemble Method: Random Forest
        recall_rfc_i = classifier(trainX, trainY, testX, testY, rfc, i)
        rfc_pr_ar.append(recall_rfc_i)
        # Nearest Neighbors: K-Nearest Neighbors
        recall_nknc_i = classifier(trainX, trainY, testX, testY, nknc, i)
        nknc_pr_ar.append(recall_nknc_i)
        # Linear Model: Logistic Regression
        recall_lr_i = classifier(trainX, trainY, testX, testY, lr, i)
        lr_pr_ar.append(recall_lr_i)
        # Support Vector Machine: LinearSVC
        recall_lsvc_i = classifier(trainX, trainY, testX, testY, lsvc, i)
        lsvc_pr_ar.append(recall_lsvc_i)
        
        i += 1

    d = {}
    d[gnb] = average(gnb_pr_ar)
    d[rfc] = average(rfc_pr_ar)
    d[nknc] = average(nknc_pr_ar)
    d[lr] = average(lr_pr_ar)
    d[lsvc] = average(lsvc_pr_ar)
    t = PrettyTable(['classifier', 'recall'])
    for key, value in d.items():
        t.add_row([key, value])
    print(t)

    the_classifier = get_key(d,max(d.values()))
    classifier2(origX2, the_classifier)


def get_key(dictionary, val):
    for key, value in dictionary.items():
         if val == value:
             return key


def average(lst):
    avg = sum(lst)/len(lst)
    return round(avg,2)


def classifier2(X, classifier2):
    # classifier2 = pickle.loads(s)
    predict = classifier2.predict(X)
    print("Choosed classifier:",classifier2)
    print("Result of classification:",predict)

    predict2 = classifier2.predict_proba(X)
    print(predict2.item(0))
    print(predict2.item(1))


def classifier(trainX, trainY, testX, testY, classifier, i):
    # global s
    classifier.fit(trainX, trainY)
    recall_i = round(test_bmodel(testX, testY, classifier),2)
    # s = pickle.dumps(classifier)
    print(i,"\t",recall_i,"\t",classifier)
    return recall_i


def test_bmodel(X, Y, classifier):
    """This method tests a classifier using test data.
    
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
    opts = [opt for opt in sys.argv[1:] if opt.startswith("-")]
    args = [arg for arg in sys.argv[1:] if not arg.startswith("-")]

    if "-x" in opts and "-y" in opts and "-z" in opts:
        for i, arg in enumerate(sys.argv):
            if i == 2:
                parameter1 = arg
            if i == 4:
                parameter2 = arg
            if i == 6:
                parameter3 = arg
        sys.exit(main(parameter1, parameter2, parameter3))
    elif "-h" in opts:
        print("Usage: "+sys.argv[0]+" [-h] [-x filename] [-y filename] [-z filename]\n\nThe parsing commands lists.\n\nMandatory arguments:\n\t-x\tnumpy file of vector X for learning\n\t-y\tnumpy file of vector Y for learning\n\t-z\tnumpy file of vector X for prediction\n\nOptional argument:\n\t-h\tprint this help message")
    else:
        raise SystemExit(f"Usage: {sys.argv[0]} [-h] [-x filename] [-y filename] [-z filename]")