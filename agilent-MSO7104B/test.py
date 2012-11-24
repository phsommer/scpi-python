#!/usr/bin/python
import time

import matplotlib
matplotlib.use('PDF')
import matplotlib.pyplot as plt

from pylab import *
from types import *
from numpy import array

import SCPI

# font settings
rcParams['pdf.use14corefonts'] = True
rcParams['font.family'] = 'serif'
rcParams['font.serif'] = 'Helvetica'
rcParams['ps.useafm'] = True
rcParams['axes.unicode_minus'] = False



# open remote measurement device (replace "hostname" by its actual name)
device = SCPI.SCPI("hostname")


y = list()

timebase = 0.1 # timebase in seconds
slices = 20 # number of measurements
channel = 1 

# setup device for measurement
device.setup(timebase, channel)

for i in range(slices):
  print time.time()
  voltage = 1000*device.measure(channel)
  y.extend(voltage)
  print time.time()
	

t = np.arange(0,slices*timebase , timebase/1000.0)

# calculate average
avg = mean(y)
print "Average current consumption:", avg

plt.figure(figsize=(10,3))
plt.plot(t, y, 'k-')
plt.axhline(y=avg, linewidth=1, linestyle='--', color='r')
plt.ylabel('Current [mA]', fontsize=10)
plt.xlabel('Time [s]', fontsize=10)
plt.xticks(fontsize=8) 
plt.yticks(fontsize=8)
plt.savefig("measurement.pdf", bbox_inches='tight')



