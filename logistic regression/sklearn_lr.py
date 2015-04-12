import numpy as np
import pylab as pl
from sklearn import linear_model
from sklearn.metrics import roc_curve, auc
import os

def interlist(a, b):
    count=0
    for i in range(len(a)):
        if a[i] == b[i]:
            count = count+1
    return count
    

AUC = []
filepath = 'E:/MF/mltask'
if(os.path.exists(filepath)):
    train = np.loadtxt(filepath+'/train.data')
    X_train = train[:,0:15]
    Y_train = train[:,15]
    test = np.loadtxt(filepath+'/test.data')
    X_test = test[:,0:15]
    Y_test = test[:,15]
    classifier = linear_model.LogisticRegression(C=1e6)
    probas = classifier.fit(X_train, Y_train)
    #probas_test = probas.predict_proba(X_test)
    preClass = probas.predict(X_test);
    print preClass
    print Y_test
    print interlist(preClass,Y_test)
    precision = interlist(preClass,Y_test)*1.0/len(Y_test)
    print precision
    


