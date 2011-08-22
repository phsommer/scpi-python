import socket
import time
import struct

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
	
    def setVoltage(self, channel, voltage):
        #set output voltage
        self.s.send("VOLTage %.2f,(@%d)\n"%(voltage,channel,))

    def setCurrent(self, channel, voltage):
        #set current
        self.s.send("CURR %.2f,(@%d)\n"%(voltage,channel,))

    def setOutput(self, channel, status):
        if status:
            #enable the output
            self.s.send("OUTPut ON,(@" + str(channel) + ")\n")
        else:
            self.s.send("OUTPut OFF,(@" + str(channel) + ")\n")

    def startCurrentMeasurement(self, channel, samples):
        self.s.send("SENS:SWE:TINT 0.001024,(@" + str(channel) + ")\n")
        self.s.send("SENS:SWE:POIN " + str(samples) + ",(@" + str(channel) + ")\n")
        self.s.send("MEAS:ARR:CURR? (@" + str(channel) + ")\n")
        

    def getCurrentMeasurements(self, channel, samples):
        self.s.settimeout(1)
        buf = []

        while True:

          try:
            data = self.s.recv(1024)
            buf.append(data)
          except socket.timeout:
            break

        self.s.settimeout(None)
        records = "".join(buf).split(',')


        data = list()
        
        for entry in records:
          try:
            data.append(float(entry.strip(' \r\n')))
          except ValueError:
            print "Error: ", entry
        return data


    def getCurrent(self, channel):
        self.s.send("MEAS:CURR? (@" + str(channel) + ")\n")
        self.s.send("FETC:CURR? (@" + str(channel) + ")\n")
	c = self.s.recv(1024)
        return c

