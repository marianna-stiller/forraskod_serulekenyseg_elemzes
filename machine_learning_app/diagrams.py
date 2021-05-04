import matplotlib.pyplot as plt
import numpy as np
import itertools
import sys
import matplotlib.pyplot as plt
from sklearn import datasets

from sklearn.metrics import confusion_matrix
from sklearn.model_selection import RepeatedStratifiedKFold
from sklearn.metrics import precision_recall_fscore_support
from sklearn.ensemble import ExtraTreesClassifier, GradientBoostingClassifier
from sklearn.naive_bayes import GaussianNB
from sklearn.calibration import calibration_curve
from sklearn.tree import DecisionTreeClassifier
from sklearn.neighbors import KNeighborsClassifier
from sklearn.linear_model import LogisticRegression
from sklearn.ensemble import RandomForestClassifier
from sklearn.svm import LinearSVC

gnb = GaussianNB()
etc = ExtraTreesClassifier()
gbc = GradientBoostingClassifier()
dtc = DecisionTreeClassifier()
nknc = KNeighborsClassifier()
lr = LogisticRegression()
svc = LinearSVC(C=1.0)


def main(argv=None):
    if argv is None:
        argv = sys.argv

    # origX = np.load("testX.npy")
    # origY = np.load("testy.npy").astype(int)
    # kFold = RepeatedStratifiedKFold(n_splits=5, n_repeats=5)
    # for train_index, validation_index in kFold.split(origX, origY):
    #     trainX, validationX = origX[train_index], origX[validation_index]
    #     trainY, validationY = origY[train_index], origY[validation_index]

    #     plot_classification(trainX, trainY, validationX, validationY)        
    #     Classifier = classifier(trainX, trainY)
    #     confusionm(validationX, validationY, Classifier)

    X, y = datasets.make_classification(n_samples=100000, n_features=20, n_informative=2, n_redundant=2)
    train_samples = 100
    X_train = X[:train_samples] # 100
    X_test = X[train_samples:] # 99.900
    y_train = y[:train_samples] # 100
    y_test = y[train_samples:] # 99.900
    plot_classification(X_train, y_train, X_test, y_test)
    Classifier = classifier(X_train, y_train)
    confusionm(X_test, y_test, Classifier)


def classifier(X, Y):
    myClassifier = etc
    myClassifier.fit(X, Y)
    return myClassifier


def confusionm(X, Y, classifier):
    """ """
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


def plot_classification(X_train, y_train ,X_test, y_test):
    plt.figure(figsize=(10, 10))
    ax1 = plt.subplot2grid((3, 1), (0, 0), rowspan=2)
    ax2 = plt.subplot2grid((3, 1), (2, 0))

    ax1.plot([0, 1], [0, 1], "k:", label="Perfectly calibrated")
    for clf, name in [  (gnb, 'Naive Bayes'), 
                        (etc, 'Extra Trees'), 
                        (gbc, 'Gradient Boostring'),
                        (dtc, 'Decision Tree'),
                        (nknc, 'NK Neighbors'), 
                        (lr, 'Logistic Regression'),
                        (svc, 'Linear SVC')
                     ]:
        clf.fit(X_train, y_train)
        if hasattr(clf, "predict_proba"):
            prob_pos = clf.predict_proba(X_test)[:, 1]
        else:
            prob_pos = clf.decision_function(X_test)
            prob_pos = \
                (prob_pos - prob_pos.min()) / (prob_pos.max() - prob_pos.min())
        fraction_of_positives, mean_predicted_value = \
            calibration_curve(y_test, prob_pos, n_bins=10)

        ax1.plot(mean_predicted_value, fraction_of_positives, "s-",
                label="%s" % (name, ))

        ax2.hist(prob_pos, range=(0, 1), bins=10, label=name,
                histtype="step", lw=2)

    ax1.set_ylabel("Fraction of positives")
    ax1.set_ylim([-0.05, 1.05])
    ax1.legend(loc="lower right")
    ax1.set_title('Calibration plots  (reliability curve)')

    ax2.set_xlabel("Mean predicted value")
    ax2.set_ylabel("Count")
    ax2.legend(loc="upper center", ncol=2)

    plt.tight_layout()
    plt.show()

if __name__ == "__main__":
    sys.exit(main())