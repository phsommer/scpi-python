#!/usr/bin/python
import SCPI
import time
from pylab import *
from types import *
from numpy import array


# open remote measurement device (replace "hostname" by its actual name)
device = SCPI.SCPI("hostname")


#setup voltage meter
device.setVoltage(1, 3.7)
device.setCurrent(1, 0.1)

# enable output
device.setOutput(1,True)


print "Start measurement..."
device.startCurrentMeasurement(1, 30000);

time.sleep(35)
print "Collect data..."
current = device.getCurrentMeasurements(1, 30000)

time = 0

# plot data
for item in current:
  print str(time) + " " + str(item) + "\n"
  time = time + 0.001


