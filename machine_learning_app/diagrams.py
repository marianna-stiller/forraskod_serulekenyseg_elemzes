import matplotlib.pyplot as plt
import numpy as np
import itertools
import sys
import matplotlib.pyplot as plt
from sklearn import datasets

from sklearn.metrics import confusion_matrix
from sklearn.calibration import calibration_curve
from sklearn.datasets import make_moons, make_circles, make_classification
from sklearn.preprocessing import StandardScaler
from sklearn.model_selection import train_test_split
from matplotlib.colors import ListedColormap

from sklearn.naive_bayes import GaussianNB
from sklearn.ensemble import RandomForestClassifier
from sklearn.neighbors import KNeighborsClassifier
from sklearn.linear_model import LogisticRegression
from sklearn.svm import LinearSVC

gnb = GaussianNB()
rfc = RandomForestClassifier()
knc = KNeighborsClassifier()
lr = LogisticRegression()
svc = LinearSVC(C=1.0)

def main(argv=None):
    if argv is None:
        argv = sys.argv

    plot_classifier_comparison()

    origX = np.load("testX.npy")
    origY = np.load("testy.npy").astype(int)
    X_train, X_test, y_train, y_test = train_test_split(origX, origY, test_size=0.2)
    plot_classification(X_train, y_train, X_test, y_test, 102)
    Classifier = classifier(X_train, y_train, gnb)
    confusionm(X_test, y_test, Classifier, 102)
  
    X, y = datasets.make_classification(n_samples=100000, n_features=20, n_informative=2, n_redundant=2)
    train_samples = 100
    X_train = X[:train_samples] # 100
    X_test = X[train_samples:] # 99.900
    y_train = y[:train_samples] # 100
    y_test = y[train_samples:] # 99.900
    plot_classification(X_train, y_train, X_test, y_test, 100000)
    Classifier = classifier(X_train, y_train, gnb)
    confusionm(X_test, y_test, Classifier, 100000)


def classifier(X, Y, classifier):
    myClassifier = classifier
    myClassifier.fit(X, Y)
    return myClassifier

def confusionm(X, Y, classifier, title):
    """This method make confusion matrix"""
    Y_pred = np.argmax(classifier.predict_proba(X), axis=1)

    # Compute confusion matrix
    classes = ['vulnerable', 'not vulnerable']
    confusion_m = confusion_matrix(Y,Y_pred,labels=[0,1])
    np.set_printoptions(precision=2)

    # Plot non-normalized confusion matrix
    plot_confusion_matrix(confusion_m, target_names=classes, title='Confusion matrix, without normalization for '+str(title)+' samples', cmap=plt.cm.Blues)

    # Plot normalized confusion matrix
    plot_confusion_matrix(confusion_m, target_names=classes, title='Normalized confusion matrix for '+str(title)+' samples', cmap=plt.cm.Blues, normalize=True)


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


def plot_classification(X_train, y_train ,X_test, y_test, title):
    plt.figure(figsize=(10, 10))
    ax1 = plt.subplot2grid((3, 1), (0, 0), rowspan=2)
    ax2 = plt.subplot2grid((3, 1), (2, 0))

    ax1.plot([0, 1], [0, 1], "k:", label="Perfectly calibrated")
    for clf, name in [  (gnb, 'Gaussian Naive Bayes'), 
                        (rfc, 'Random Forest'), 
                        (knc, 'K-Nearest Neighbors'), 
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
    ax1.set_title('Reliability curve for '+str(title)+' samples')

    ax2.set_xlabel("Mean predicted value")
    ax2.set_ylabel("Count")
    ax2.legend(loc="upper center", ncol=2)

    plt.tight_layout()
    plt.show()

def plot_classifier_comparison():
    h = .02  # step size in the mesh

    names = ["Gaussian Naive Bayes", "Random Forest", "K-Nearest Neighbors", 
    "Logistic Regression", "LinearSVC"]

    classifiers = [gnb, rfc, knc, lr, svc]

    X, y = make_classification(n_features=2, n_redundant=0, n_informative=2,
                            random_state=1, n_clusters_per_class=1)
    rng = np.random.RandomState(2)
    X += 2 * rng.uniform(size=X.shape)
    linearly_separable = (X, y)

    datasets = [make_moons(noise=0.3, random_state=0),
                make_circles(noise=0.2, factor=0.5, random_state=1),
                linearly_separable
                ]

    figure = plt.figure(figsize=(27, 9))
    i = 1
    # iterate over datasets
    for ds_cnt, ds in enumerate(datasets):
        # preprocess dataset, split into training and test part
        X, y = ds
        X = StandardScaler().fit_transform(X)
        X_train, X_test, y_train, y_test = \
            train_test_split(X, y, test_size=.4, random_state=42)

        x_min, x_max = X[:, 0].min() - .5, X[:, 0].max() + .5
        y_min, y_max = X[:, 1].min() - .5, X[:, 1].max() + .5
        xx, yy = np.meshgrid(np.arange(x_min, x_max, h),
                            np.arange(y_min, y_max, h))

        # just plot the dataset first
        cm = plt.cm.RdBu
        cm_bright = ListedColormap(['#FF0000', '#0000FF'])
        ax = plt.subplot(len(datasets), len(classifiers) + 1, i)
        if ds_cnt == 0:
            ax.set_title("Input data")
        # Plot the training points
        ax.scatter(X_train[:, 0], X_train[:, 1], c=y_train, cmap=cm_bright,
                edgecolors='k')
        # Plot the testing points
        ax.scatter(X_test[:, 0], X_test[:, 1], c=y_test, cmap=cm_bright, alpha=0.6,
                edgecolors='k')
        ax.set_xlim(xx.min(), xx.max())
        ax.set_ylim(yy.min(), yy.max())
        ax.set_xticks(())
        ax.set_yticks(())
        i += 1

        # iterate over classifiers
        for name, clf in zip(names, classifiers):
            ax = plt.subplot(len(datasets), len(classifiers) + 1, i)
            clf.fit(X_train, y_train)
            score = clf.score(X_test, y_test)

            # Plot the decision boundary. For that, we will assign a color to each
            # point in the mesh [x_min, x_max]x[y_min, y_max].
            if hasattr(clf, "decision_function"):
                Z = clf.decision_function(np.c_[xx.ravel(), yy.ravel()])
            else:
                Z = clf.predict_proba(np.c_[xx.ravel(), yy.ravel()])[:, 1]

            # Put the result into a color plot
            Z = Z.reshape(xx.shape)
            ax.contourf(xx, yy, Z, cmap=cm, alpha=.8)

            # Plot the training points
            ax.scatter(X_train[:, 0], X_train[:, 1], c=y_train, cmap=cm_bright,
                    edgecolors='k')
            # Plot the testing points
            ax.scatter(X_test[:, 0], X_test[:, 1], c=y_test, cmap=cm_bright,
                    edgecolors='k', alpha=0.6)

            ax.set_xlim(xx.min(), xx.max())
            ax.set_ylim(yy.min(), yy.max())
            ax.set_xticks(())
            ax.set_yticks(())
            if ds_cnt == 0:
                ax.set_title(name)
            ax.text(xx.max() - .3, yy.min() + .3, ('%.2f' % score).lstrip('0'),
                    size=15, horizontalalignment='right')
            i += 1

    plt.tight_layout()
    plt.show()

if __name__ == "__main__":
    sys.exit(main())