#!/usr/bin/python
# -*- coding: utf-8 -*-

import ols
import numpy
import pylab
import pickle

f = open('matrices.pck')

matrices = pickle.load(f)

y = numpy.matrix(matrices['y'])
X = numpy.matrix(matrices['X'])

Theta = numpy.linalg.pinv(X.T * X)*X.T*y

print 'Theta'
print Theta

print 'X', X.shape
print X

print 'y', y.shape
print y

prediction = (Theta.T * X.T).T

print 'prediction', prediction.shape
print prediction

print 'fit'
print prediction - y

y = numpy.array(matrices['y'])
X = numpy.array(matrices['X'])


X = X[:, 1:]

print 'y.shape', y.shape
print 'X.shape', X.shape

mymodelX = ols.ols(y[:, 0], X, 'ORGX', ['distance', 'wavelength'])
mymodelY = ols.ols(y[:, 1], X, 'ORGY', ['distance', 'wavelength'])

print 'mymodelX.p', mymodelX.p

mymodelX.summary()

print 'mymodelY.p', mymodelY.p

mymodelY.summary()