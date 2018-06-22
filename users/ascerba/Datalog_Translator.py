import pylab
import numpy as np
import os

fname = '/home/ascerba/Documents/DATALOG.TXT'

lines = [l for l in open(fname) if len(l) > 5]
print(lines[:10])
times = []
locs = []
alts = []
for l in lines:
    if 'Time' in l:
        while len(times) > len(locs): locs.append('')
        while len(times) > len(alts): alts.append('')
        times.append(l[6:])
    if 'Location' in l:
        locs.append(l[10:])
    if 'Altitude' in l:
        alts.append(l[10:])
    if 'Fix' in l and not 'Fix: 1 quality: 1' in l:
        print(repr(times),repr(locs),repr(alts))
        del times[-1]
        
n = len(times)
timearr = np.zeros([n])
#lonarr = np.zereos([n])
#latarr = np.zereos([n])
print(times[:5])
print(locs[:5])
print(alts[:5])
heiarr = np.zeros([n])
for i in range(n):
     # Change time to seconds since midnight
     #timearr[i] = something_of(times[i])
     # Change locs to lon/lat
     # Change altitudees
     heiarr[i] = float( alts[i].strip() )

pylab.figure()
pylab.plot(heiarr)
pylab.show()
