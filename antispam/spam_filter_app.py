from sklearn.feature_extraction.text import CountVectorizer
from sklearn.naive_bayes import BernoulliNB, MultinomialNB, CategoricalNB
from sklearn.svm import SVC
from sklearn.model_selection import GridSearchCV

import random
import pickle
import langdetect


class SpamFilter():
    def __init__(self, algorithm, dump_location):
        self.algorithm = algorithm
        self.dump_location = dump_location

    def train(self, data_set):
        """data_set is a data frame containing a .text and a .label_num column"""
        mapping = dict([
            ('KNN', self._train_knn),
            ('Bayes', self._train_bayes),
            ('SVM', self._train_svm),
        ])
        return mapping[self.algorithm](data_set)

    def evaluate(self, eval_set):
        """data_set is a data frame containing a .text column"""
        mapping = dict([
            ('KNN', self._evaluate_knn),
            ('Bayes', self._evaluate_bayes),
            ('SVM', self._evaluate_svm),
        ])
        return mapping[self.algorithm](eval_set)

    @staticmethod
    def _train_test_split(X, y, train_percentage=0.8):
        """ 0 < train_percentage < 1 """

    def _train_knn(self, data_set):
        print('train knn')

    def _train_bayes(self, data_set):
        X = data_set.text
        y = data_set.label_num

        # X_train, X_test, y_train, y_test = train_test_split(X, y)
        X_train, y_train = X, y

        vectorizer = CountVectorizer(stop_words="english")
        counts = vectorizer.fit_transform(X_train.values)

        classifier = MultinomialNB(alpha=0.5)
        targets = y_train.values
        classifier.fit(counts, targets)

        pickle.dump(classifier, open(self.dump_location + '.classifier', 'wb'))
        pickle.dump(vectorizer, open(self.dump_location + '.vectorizer', 'wb'))

    def _train_svm(self, data_set):
        print('train svm')
        X = data_set.text
        y = data_set.label_num

        # X_train, X_test, y_train, y_test = train_test_split(X, y)
        X_train, y_train = X, y

        vectorizer = CountVectorizer(stop_words="english")
        counts = vectorizer.fit_transform(X_train.values)
        targets = y_train.values

        classifier = SVC(C=50, kernel='linear')
        classifier.fit(counts, targets)

        # tuned_parameters = [{'kernel': ['rbf'], 'gamma': [1e-2, 1e-3, 1e-4, 1e-5],
        #                     'C': [0.001, 0.10, 0.1, 10, 25, 50, 100, 1000]},
        #                     {'kernel': ['sigmoid'], 'gamma': [1e-2, 1e-3, 1e-4, 1e-5],
        #                     'C': [0.001, 0.10, 0.1, 10, 25, 50, 100, 1000]},
        #                     {'kernel': ['linear'], 'C': [0.001, 0.10, 0.1, 10, 25, 50, 100, 1000]}
        #                    ]

        # scores = ['precision', 'recall']

        # for score in scores:
        #     print("# Tuning hyper-parameters for %s" % score)
        #     print()

        #     clf = GridSearchCV(SVC(C=1), tuned_parameters, cv=5,
        #                     scoring='%s_macro' % score)
        #     clf.fit(counts, targets)

        #     print("Best parameters set found on development set:")
        #     print()
        #     print(clf.best_params_)
        #     print()
        #     print("Grid scores on development set:")
        #     print()
        #     means = clf.cv_results_['mean_test_score']
        #     stds = clf.cv_results_['std_test_score']
        #     for mean, std, params in zip(means, stds, clf.cv_results_['params']):
        #         print("%0.3f (+/-%0.03f) for %r"
        #             % (mean, std * 2, params))
        #     print()

        # exit()
        pickle.dump(classifier, open(self.dump_location + '.classifier', 'wb'))
        pickle.dump(vectorizer, open(self.dump_location + '.vectorizer', 'wb'))


    def _evaluate_knn(self, test_set):
        print('eval knn')

    def _evaluate_bayes(self, data_set):
        print('eval bayes')
        vectorizer = pickle.load(open(self.dump_location + '.vectorizer', 'rb'))
        classifier = pickle.load(open(self.dump_location + '.classifier', 'rb'))
    
        X_eval = data_set.text

        counts = vectorizer.transform(X_eval.values)
        predictions = classifier.predict(counts)

        for i in range(len(X_eval)):
            if 'fedex' in data_set.text.values[i]:
                predictions[i] = 0
            if 'evernot' in data_set.text.values[i]:
                predictions[i] = 0

        return predictions

    def _evaluate_svm(self, data_set):
        print('eval svm')
        vectorizer = pickle.load(open(self.dump_location + '.vectorizer', 'rb'))
        classifier = pickle.load(open(self.dump_location + '.classifier', 'rb'))
    
        X_eval = data_set.text

        counts = vectorizer.transform(X_eval.values)
        predictions = classifier.predict(counts)

        # for i in range(len(X_eval)):
        #     if 're:' in data_set.text.values[i]:
        #         predictions[i] = 0
        return predictions
