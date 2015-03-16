#!/usr/bin/python
# -*- coding: utf-8 -*-

import pylab
import pickle
import numpy
import commands
import os

def saveMatrices():
    f = open('matrices.pck', 'w')
    pickle.dump(matrices, f)
    f.close()
    
def getAttributeValue(filename, attribute, position=-2, separator=';'):
    return float(commands.getoutput('grep %s %s' % (attribute, filename)).split(separator)[position])

#directory = '/927bis/ccd/Database/watchTheBeam/healedTables'
directory = '/927bis/ccd/gitRepos/Beamline/healedTables'
points = commands.getoutput('ls -tr %s/SuiviLigne_2015-02-1[456]*' % directory).split('\n')

print 'points[:10]'
print points[:10]

attributesOfInterestY = ['I11-MA-C04/DT/XBPM_DIODE.1/horizontalPosition',
                         'I11-MA-C04/DT/XBPM_DIODE.1/verticalPosition',
                         'I11-MA-C05/DT/XBPM_DIODE.3/horizontalPosition',
                         'I11-MA-C05/DT/XBPM_DIODE.3/verticalPosition',
                         'I11-MA-C06/DT/XBPM_DIODE.5/horizontalPosition',
                         'I11-MA-C06/DT/XBPM_DIODE.5/verticalPosition']
                         
attributesOfInterestW = ['I11-MA-C06/DT/XBPM_DIODE.5/horizontalPosition',
                         'I11-MA-C06/DT/XBPM_DIODE.5/verticalPosition']
                         
attributesOfInterestX = ['I11-MA-CX1/EX/MD2-BEAMPOSITION/Zoom10_X',
                         'I11-MA-CX1/EX/MD2-BEAMPOSITION/Zoom10_Z']

X = []
y = []
w = []
for point in points:
    pointY = []
    pointW = []
    pointX = []
    for attribute in attributesOfInterestY:
        filename = os.path.join(directory, point)
        pointY.append(getAttributeValue(filename, attribute, position=-2))
    for attribute in attributesOfInterestW:
        filename = os.path.join(directory, point)
        pointW.append(getAttributeValue(filename, attribute, position=-2))
    for attribute in attributesOfInterestX:
        filename = os.path.join(directory, point)
        pointX.append(getAttributeValue(filename, attribute, position=-3))
    y.append(pointY)
    w.append(pointW)
    X.append(pointX)
    
matrices = {'X': X, 'y': y, 'w': w}

pylab.figure()
pylab.plot(X)

pylab.figure()
pylab.plot(w)

pylab.figure()
pylab.plot(y)

pylab.show()
#print 'matrices'
print matrices
saveMatrices()