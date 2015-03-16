#!/usr/bin/env python

import pickle
import commands
import pylab
import numpy
import matplotlib.dates as mdates
import matplotlib.pyplot as plt

def load_point(filename):
    f = open(filename)
    p = pickle.load(f)
    f.close()
    return p
 
def get_value(filename, device, attribute, value):
    #print point
    point = load_point(filename)
    return point[device][attribute][value]
    
def get_values(filename):
    d1 = 'i11-ma-cx1/dt/dtc_ccd.1-mt_ts'
    d2 = 'i11-ma-c02/ex/tc.1'
    d3 = 'i11-ma-cx1/dt/dtc_ccd.1-mt_tx'
    d4 = 'i11-ma-cx1/dt/dtc_ccd.1-mt_tz'
    d5 = 'i11-ma-c00/ex/beamlineenergy'
    attribute = 'position'
    value = 'value'
    point = load_point(filename)
    distance = point[d1]['position'][value]
    x = point[d3]['position'][value]
    z = point[d4]['position'][value]
    energy = point[d5]['energy'][value]
    temp1 = point[d2]['temperature'][value]
    time = point['time']
    return time, temp1, distance, x, z, energy
    
def get_beam_positions(filename):
    point = load_point(filename)
    
    cvd = 'i11-ma-c05/dt/xbpm-cvd.1'
    b5 = 'i11-ma-c06/dt/xbpm_diode.5'
    b3 = 'i11-ma-c05/dt/xbpm_diode.3'
    b1 = 'i11-ma-c04/dt/xbpm_diode.1'
    bp = 'i11-ma-cx1/ex/md2-beamposition'
    temp1 = 'i11-ma-cx1/ex/tc.1'
    temp2 = 'i11-ma-cx1/ex/tc.2'
    v = 'value'
    
    cvd_pos_z = point[cvd]['verticalPosition'][v]
    cvd_pos_x = point[cvd]['horizontalPosition'][v]
    cvd_pos_i = point[cvd]['intensity'][v]
    
    b1_pos_z = point[b1]['verticalPosition'][v]
    b1_pos_x = point[b1]['horizontalPosition'][v]
    b1_pos_i = point[b1]['intensity'][v]
    
    b3_pos_z = point[b3]['verticalPosition'][v]
    b3_pos_x = point[b3]['horizontalPosition'][v]
    b3_pos_i = point[b3]['intensity'][v]
    
    b5_pos_z = point[b5]['verticalPosition'][v]
    b5_pos_x = point[b5]['horizontalPosition'][v]
    b5_pos_i = point[b5]['intensity'][v]    
    
    bp_pos_z = point[bp]['Zoom10_Z'][v]
    bp_pos_x = point[bp]['Zoom10_X'][v]
    
    t1 = point[temp1]['temperature'][v]
    t2 = point[temp2]['temperature'][v]
    
    time = point['time']
    
    return time, bp_pos_x, cvd_pos_x, b5_pos_x, b3_pos_x, b1_pos_x, bp_pos_z, cvd_pos_z, b5_pos_z, b3_pos_z, b1_pos_z, cvd_pos_i, b5_pos_i, b3_pos_i, b1_pos_i, t1, t2
    
    
def getval(p, device, attribute, value):
    return p[device][attribute][value]
    

directory = '/927bis/ccd/gitRepos/Beamline'
directory2 = '/927bis/ccd/gitRepos/Beamline/crontab_points'
#directory3 = '/927bis/ccd/gitRepos/Beamline'
template = 'point_*_[MF]??_[12][0123456789]*2015.pck'



try: 
    f = open('history.pck')
    h_old = pickle.load(f)
    f.close()
except:
    h_old = None
   
try:
    f = open('filenames.pck')
    old_filenames = pickle.load(f)
    f.close()
except:
    old_filenames = set([])

all_filenames = set(commands.getoutput('ls -tr %s/%s' % (directory, template)).split('\n'))
#ball_filenames = set([]) #commands.getoutput('ls -tr %s/%s' % (directory2, template)).split('\n'))
#all_filenames = all_filenames.union(ball_filenames)

print 'all' , len(all_filenames)
filenames = all_filenames - old_filenames
print 'young', len(filenames)
print filenames

#filenames = old_filenames

fnames = list(filenames)
fnames.sort()
history = [get_beam_positions(filename) for filename in fnames]
#history.sort()

h = numpy.array(history)

#h = h_old

#print h.shape
print 'h.shape', h.shape
if h_old is not None and h.shape[0] > 0:
    print 'h_old.shape', h_old.shape
    h = numpy.vstack((h_old, h))
elif h_old is not None:
    print 'h_old.shape', h_old.shape
    h = h_old
else:
    print 'should not happen'

#h.sort()

#f = open('history.pck', 'w')
#pickle.dump(h, f)
#f.close()

#f = open('filenames.pck', 'w')
#pickle.dump(all_filenames, f)
#f.close()

time, bp_pos_x, cvd_pos_x, b5_pos_x, b3_pos_x, b1_pos_x, bp_pos_z, cvd_pos_z, b5_pos_z, b3_pos_z, b1_pos_z, cvd_pos_i, b5_pos_i, b3_pos_i, b1_pos_i, t1, t2 = range(17)
#pylab.plot(h[:,0], h[:, 1], label='horizontal')
calib = numpy.array((0.000338, 0.000341))

time = h[:,time]
oav = h[:, bp_pos_z] * calib[1] * 1000
cvd = h[:, cvd_pos_z] * 1000
t1 = h[:, t1]
t2 = h[:, t2]
b5 = h[:, b5_pos_z] * 1000
b3 = h[:, b3_pos_z] * 1000
b1 = h[:, b1_pos_z] * 1000

ti5 = time[b5<0.8*b5.max()]
b5 = b5[b5<0.8*b5.max()]

cvd = -cvd
b3 = -b3
oav = (oav - oav.mean()) #/ oav.std() #+ 8 #/ oav.std()
cvd = (cvd - cvd.mean()) #/ cvd.std() #+ 4 #/ oav.std()
b5 = (b5 - b5.mean()) - 1 #/ b5.std() -1
b3 = (b3 - b3.mean()) - 2 #/ b3.std() -2
b1 = (b1 - b1.mean()) - 3 # / b1.std() 
t1 = (t1 - t1.mean()) - 4
t2 = (t2 - t2.mean()) - 5


years    = mdates.YearLocator()   # every year
months   = mdates.MonthLocator()  # every month
days     = mdates.DayLocator()
hours    = mdates.HourLocator()
yearsFmt = mdates.DateFormatter('%Y-%m-%d %H:%M')

#fig = plt.figure()
#fig.suptitle('Beam vertical position')
#ax = fig.add_subplot(1,1,1)
#ax.plot(time, oav, label='oav')
#ax.plot(time, t1, label='temp1')
#ax.plot(time, t2, label='temp2')
##ax.format_xdata = mdates.DateFormater('%Y-%m-%d')
#ax.grid(True)
#fig.autofmt_xdate()
#plt.show()

import datetime
import time as tmodule
import re

dewar_fillings = commands.getoutput('grep Filling errors*log').split('\n')
#print dewar_fillings
d_times = []
d_values = []

for record in dewar_fillings:
    t = re.findall('\[(.*)\].*', record)[0]
    t = tmodule.mktime(tmodule.strptime(t, '%b %d %Y %H:%M:%S'))
    d_times += [t, t]
    if 'begin' in record:
        d_values += [-6, 6]
    elif 'end' in record:
        d_values += [6, -6]
    else:
        print 'probleme: ni l\'un ni l\'autre'

d_times = map(datetime.datetime.fromtimestamp, d_times)
time = map(datetime.datetime.fromtimestamp, time)
ti5 = map(datetime.datetime.fromtimestamp, ti5)

pylab.figure()
pylab.title('Beam vertical position')
print oav
print len(oav)
pylab.plot_date(time, oav, label='oav', lw=2, fmt='g-')
pylab.plot_date(time, cvd, label='cvd', fmt='c-')
pylab.plot_date(ti5, b5, label='b5', fmt='y-')
pylab.plot_date(time, b3, label='b3', fmt='-', color='#afeeee')
pylab.plot_date(time, b1, label='b1', fmt='m-')
pylab.plot_date(time, t1, label='temp1', fmt='b-')
pylab.plot_date(time, t2, label='temp2', fmt='r-')
pylab.plot_date(d_times, d_values, label='dewar filling', fmt='k-')
pylab.xlabel('time')
pylab.legend(loc=3)
pylab.grid(True)
pylab.show()