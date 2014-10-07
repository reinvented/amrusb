#!/usr/bin/env python

import serial
import time
import sys

from time import strftime

class App():

    def __init__(self):
        self.device = '/dev/ttyACM0'

    def run(self):
        ser = serial.Serial(self.device)
        while True:
            try:
                line = ser.readline().rstrip()
            except:
                print 'Could not read from the AMRUSB-1'
                print sys.exc_info()[0]
            else:
                print line

app = App()
app.run()
