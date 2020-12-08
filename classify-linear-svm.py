from classify import *

print('************ classify new sequences ************************')

k = 7
# classifiers = ['linear-svm', 'poly-svm', 'rbf-svm', 'LinearDiscriminant', 'KNN']
classifiers = ['linear-svm']


for classifier in classifiers:
    pipeline = training(train, k, classifier)
    acc = testing(test, k, pipeline)
    print(classifier+":", acc)