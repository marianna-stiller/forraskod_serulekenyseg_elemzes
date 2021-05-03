import matplotlib.pyplot as plt
import numpy as np
import itertools
import sys

from sklearn.metrics import confusion_matrix
from sklearn.model_selection import RepeatedStratifiedKFold
from sklearn.ensemble import ExtraTreesClassifier
from sklearn.metrics import precision_recall_fscore_support


def main(argv=None):
    if argv is None:
        argv = sys.argv

    origX = np.load("testX.npy")
    origY = np.load("testy.npy").astype(int)
    
    kFold = RepeatedStratifiedKFold(n_splits=5, n_repeats=5)

    for train_index, validation_index in kFold.split(origX, origY):
        trainX, validationX = origX[train_index], origX[validation_index]
        trainY, validationY = origY[train_index], origY[validation_index]

        Classifier = classifier(trainX, trainY)
        test_bmodel(validationX, validationY, Classifier)


def classifier(X, Y):
    myClassifier = ExtraTreesClassifier()
    myClassifier.fit(X, Y)
    return myClassifier

def test_bmodel(X, Y, classifier):
    Y_pred = np.argmax(classifier.predict_proba(X), axis=1)

    # Compute confusion matrix
    classes = ['vulnerable', 'not vulnerable']
    confusion_m = confusion_matrix(Y,Y_pred,labels=[0,1])
    np.set_printoptions(precision=2)

    # Plot non-normalized confusion matrix
    plot_confusion_matrix(confusion_m, target_names=classes, title='Confusion matrix, without normalization', cmap=plt.cm.Blues)

    # Plot normalized confusion matrix
    plot_confusion_matrix(confusion_m, target_names=classes, title='Normalized confusion matrix', cmap=plt.cm.Blues, normalize=True)


def plot_confusion_matrix(cm, target_names, title='Confusion matrix', cmap=plt.cm.Blues, normalize=False):
    """ This method make the plots.

        Parameters:
        -----------
        cm              : confusion matrix from sklearn.metrics.confusion_matrix
        target_names    : given classification classes such as [0, 1, 2] the class names, for example: ['high', 'medium', 'low']
        title           : the text to display at the top of the matrix
        cmap            : the gradient of the values displayed from matplotlib.pyplot.cm
                            plt.get_cmap('jet') or plt.cm.Blues
        normalize       : if False, plot the raw numbers; if True, plot the proportions

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