#!/usr/bin/python


from Gpib import *
from time import sleep
from numpy import *
import sys
import pylab as pl
from libnienet import *


# replace with hostname of the device
host = "hostname"
l = EnetLib(host)

# connect to device
ud = l.ibdev(pad=3,sad=0, tmo=10, eot=1, eos=0) # primary address = 3 (GPIB)

# clear device
l.ibclr(ud)

# reset device
l.ibwrt(ud, "*RST")

# get device identification
l.ibwrt(ud, "*IDN?")
[status, response] = l.ibrd(ud, 4096)
print "Device found: ", response


# set trigger level to 1.4V on both channels
stat = l.ibwrt(ud, ":SENSe:EVENt1:LEVEL 1.4")
stat = l.ibwrt(ud, ":SENSe:EVENt2:LEVEL 1.4")

# format response as ASCII
l.ibwrt(ud, ":FORMat:DATA ASCii")
# measure interval between rising edge on channel 1 and 2
l.ibwrt(ud, ":SENSe:FUNCtion \"TINTerval 1,2\"")

# start continuous measurement
l.ibwrt(ud, ":SENSe:TINTerval:ARM:SOURce IMMediate")
l.ibwrt(ud, ":INITiate:CONTinuous ON")

# wait
sleep(1)

# perform continuous measurements
while True:
    l.ibwrt(ud, ":FETCH?")
    sleep(0.25)
    [status, result] = l.ibrd(ud, 4096)
    try:
        print "Interval[s]:", float(result)
    except ValueError:
        print "Not valid:", result

# disconnect
l.ibonl(ud, 1)

