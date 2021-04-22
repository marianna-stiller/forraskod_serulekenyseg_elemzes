# -*- coding: utf-8 -*-
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

    """ Preparing and caller section of the classifier """

   # Import dataset
    origX = np.load("testX.npy")
    origY = np.load("testy.npy").astype(int)
    origX2 = np.load("toimportX.npy")
    origY2 = np.load("toimporty.npy").astype(int)

    kFold = RepeatedStratifiedKFold(n_splits=5, n_repeats=5) # n_samples=102

    for train_index, validation_index in kFold.split(origX, origY):
        trainX, validationX = origX[train_index], origX[validation_index]
        trainY, validationY = origY[train_index], origY[validation_index]

        # Create classifier for a specific class
        Classifier = classifier(trainX, trainY)
        # Test the binary model
        results = test_bmodel(validationX, validationY, Classifier)
        #print(results)

    classifier2(origX2,origY2)

def classifier2(X, Y):
    # Load the pickled model
    myClassifier2 = pickle.loads(s)

    predict1 = myClassifier2.predict_proba(X)
    predict2 = myClassifier2.predict(X)

    print(predict1.item(0))
    print(predict1.item(1))
    print(myClassifier2.classes_)
    print(predict1)
    print(predict2)

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

    """ argmax
    
        Returns the indices of the maximum values along an axis.
        Parameters:
        -----------
        a       : input array
        axis    : by default, the index is into the flattened array, otherwise along the specified axis
    """
    Y_pred = np.argmax(classifier.predict_proba(X), axis=1)
    # Evaluate
    """precision_recall_fscore_support
    
        Returns: precision, recall, fbeta_score, support
        Parameters:
        -----------
        Y       : ground truth (correct) target values.
        Y_pred  : estimated targets as returned by a classifier.
        pos_label: setting labels=[pos_label] and average!='binary' will report scores for that label only.
        average ('micro')   : calculate metrics globally by counting the total true positives, false negatives and false positives. 
    """

    classes = ['vulnerable', 'not vulnerable']
    # Compute confusion matrix
    #print("Y:",Y)
    #print("Y_pred:",Y_pred)
    confusion_m = confusion_matrix(Y,Y_pred,labels=[0,1])
    np.set_printoptions(precision=2)

    # Plot non-normalized confusion matrix
    # plot_confusion_matrix(confusion_m, target_names=classes, title='Confusion matrix, without normalization', cmap=plt.cm.Blues)

    # Plot normalized confusion matrix
    # plot_confusion_matrix(confusion_m, target_names=classes, title='Normalized confusion matrix', cmap=plt.cm.Blues, normalize=True)

    evaluation = precision_recall_fscore_support(Y, Y_pred, pos_label=1, average='micro')

    return evaluation

def plot_confusion_matrix(cm, target_names, title='Confusion matrix', cmap=plt.cm.Blues, normalize=False):
    """
    given a sklearn confusion matrix (cm), make a nice plot

    Parameters:
    -----------
    cm              : confusion matrix from sklearn.metrics.confusion_matrix
    target_names    : given classification classes such as [0, 1, 2] the class names, for example: ['high', 'medium', 'low']
    title           : the text to display at the top of the matrix
    cmap            : the gradient of the values displayed from matplotlib.pyplot.cm
                        plt.get_cmap('jet') or plt.cm.Blues
    normalize       : If False, plot the raw numbers; If True, plot the proportions

    """

    plt.figure()
    plt.imshow(cm, interpolation='nearest', cmap=cmap)
    plt.title(title)
    plt.colorbar()
    tick_marks = np.arange(len(target_names))
    plt.xticks(tick_marks, target_names, rotation=45)
    plt.yticks(tick_marks, target_names)

    if normalize:
        cm = cm.astype('float') / cm.sum(axis=1)[:, np.newaxis]
        print("Normalized confusion matrix")
    else:
        print("Confusion matrix, without normalization")

    print(cm)

    thresh = cm.max() / 2
    for i, j in itertools.product(range(cm.shape[0]), range(cm.shape[1])):
        plt.text(j, i, cm[i, j],
            horizontalalignment="center",
            color="white" if cm[i, j] > thresh else "black")

    plt.tight_layout()
    plt.ylabel('True label')
    plt.xlabel('Predicted label')
    plt.show()

if __name__ == "__main__":
    sys.exit(main())