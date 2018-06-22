""" Datalog_Translator.py

    Translates the raw file from the feather with GPS into a Tab delimited
    data file.
"""

import pylab
import numpy as np
import os
import sys
import math

# get fname as first argument (optional)
print(sys.argv)
if len(sys.argv) > 1:
    fname = sys.argv[1]
else:
    fname = '/home/ascerba/github_repos/techcamp/users/ascerba/DATALOG.TXT'

# Open file and read lines
lines = [l for l in open(fname) if len(l) > 5]
# Put data in lists
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
    if 'Fix' in l and not 'Fix: 1 quality:' in l:
        del times[-1]

if len(times) != len(locs) or len(times) != len(alts):
    print("Error: Arrays of unequal lengths:", len(times), len(locs), len(alts))
    exit(1)
print(times[:5])
print(locs[:5])
print(alts[:5])
n = len(times)
# Move Data into arrays
timearr = np.zeros([n])
lonarr = np.zeros([n])
latarr = np.zeros([n])
heiarr = np.zeros([n])
for i in range(n):
     # Change time to seconds since midnight times[i] = '3:33:30.933\r\n'
     h,m,s = [int(j) for j in times[i].split('.')[0].split(':') ] # get only HH:MM:SS part
     timearr[i] = 3600*h+60*m+s
     # Change locs to lon
     lat,lon = [float(s.strip()[:-1])/100. for s in locs[i].split(',')]
     lonarr[i] = math.trunc(lon)
     lonarr[i] += 100*(lon-lonarr[i])/60.
     latarr[i] = math.trunc(lat)
     latarr[i] += 100*(lat-latarr[i])/60.
     # Change altitudees
     heiarr[i] = float( alts[i].strip() )


pylab.figure()
pylab.subplot(4,1,1)
pylab.plot(timearr, heiarr)
pylab.ylabel("Height - Raw")

### Rescale time data (to start at 0)
timearr = timearr-timearr[0]
### Filter height data
heimed = np.median(heiarr)
# Check altitude 100x higher -> fix it
for i in range(1,n-1):
    if heiarr[i] > 20*heimed:
        heiarr[i] = heiarr[i] / 100
# Check altitude 0 with neighboring values good -> fix it
for i in range(1,n-1):
    if heiarr[i] == 0 and heiarr[i-1] > 0 and heiarr[i+1] > 0:
        heiarr[i] = ( heiarr[i-1]+heiarr[i+1] ) / 2

### Filter lon/lat data: change to meters from average
# Use approximation that 1 deg is 111111meters
lonmed = np.median(lonarr)
latmed = np.median(latarr)
lonarr -=lonmed
latarr -=latmed
lonarr *= 111111.1
latarr *= 111111.1 * math.cos(math.pi * latmed / 180.)

# Save File
outf = open(fname.replace('.TXT','_Red.TXT'),'wt')
outf.write('Time\tLon\tLat\tHei\r\n')
for i in range(n):
    outf.write('%5.1f\t%6.1f\t%6.1f\t%6.1f\r\n' % (timearr[i], lonarr[i], latarr[i], heiarr[i]))
outf.close()

# Plots
pylab.subplot(4,1,2)
pylab.plot(timearr, heiarr)
pylab.plot(timearr, heiarr, 'rd')
pylab.ylabel("Height - Filtered")
pylab.subplot(4,1,3)
pylab.plot(timearr, lonarr)
pylab.ylabel("Long")
pylab.subplot(4,1,4)
pylab.plot(timearr, latarr)
pylab.ylabel("Lat")
pylab.show()
