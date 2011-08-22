#!/usr/bin/python


from Gpib import *
from time import sleep
from numpy import *
import sys
import pylab as pl
from libnienet import *


# replace with hostname of the device
host = "hostname"

# connect to device over GPIB/Ethernet
l = EnetLib(host)
ud = l.ibdev(pad=3,sad=0, tmo=10, eot=1, eos=0) # primary address = 3 (GPIB)

# clear device
l.ibclr(ud)

# reset device
l.ibwrt(ud, "*RST")

# get device identification
l.ibwrt(ud, "*IDN?")
[status, response] = l.ibrd(ud, 4096)
print "Device found: ", response


# configure frequency measurement
l.ibwrt(ud, ":CONF:FREQ 1MHz, 0.001 HZ, (@1)")

# start measurement
l.ibwrt(ud, ":READ?")

# wait for result
sleep(5)

[status, result] = l.ibrd(ud, 4096)
print "Frequency[Hz]:", float(result)

# disconnect
l.ibonl(ud, 1)
