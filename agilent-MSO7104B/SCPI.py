import socket
import time
import struct
import numpy as np
import sqlite3
from pylab import *
from types import *
from numpy import array




# Based on mclib by Thomas Schmid (http://github.com/tschmid/mclib)

class SCPI:
    PORT = 5025

    def __init__(self, host, port=PORT):
        self.host = host
        self.s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.s.connect((host, port))

	self.f = self.s.makefile("rb")


    def reset(self):
        # reset and clear device
        self.s.send("*RST\n")
        self.s.send("*CLS\n")
	self.s.send(":AUTOSCALE\n")
	#self.s.send(":STOP\n")

    def getIdent(self):
        self.s.send("*IDN?\n")

        try:
            data = self.s.recv(1024)
            return data
        except socket.timeout:
            return ""

    def setup(self, timebase, channel):
	self.s.send(":ACQUIRE:TYPE HRESolution\n")
	self.s.send(":TIMEBASE:MODE MAIN\n")
	self.s.send(":TIMEBASE:RANG " + str(timebase) + "\n")
	self.s.send(":WAVeform:SOURce CHANnel" + str(channel) + "\n")
	self.s.send(":WAVeform:FORMat ASCii\n")
	self.s.send(":WAVeform:POINts 1000\n")

    def measure(self, channel):

	self.s.send(":DIGitize CHANnel" + str(channel) + "\n")
	self.s.send(":WAVeform:DATA?\n")

        try:
            data = ""
 	    while (not data.endswith('\n')):
              data += self.s.recv(1024)
	    
        except socket.timeout:
            return None

        data = data.split(' ')
	data = data[1:len(data)]
	

     	data = np.array(data, dtype='S11')

	voltage = data.astype(np.float)

        return voltage

