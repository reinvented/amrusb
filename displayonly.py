#!/usr/bin/env python

import serial
import logging
import time
import sys

from time import strftime

class App():

    def __init__(self):
        self.device = '/dev/ttyACM0'
        self.stdin_path = '/dev/null'
        self.stdout_path = '/dev/tty'
        self.stderr_path = '/dev/tty'
        self.pidfile_path =  '/var/run/amrusb/amrusb.pid'
        self.pidfile_timeout = 5

    def run(self):
        logger.info('Starting amrusb daemon')
        logger.info('Opening device ' + self.device)
        ser = serial.Serial(self.device)
        while True:
            try:
                line = ser.readline().rstrip()
            except:
                logger.error('Could not read from the AMRUSB-1');
                logger.error(sys.exc_info()[0])
            else:
                logger.info(line)

app = App()
logger = logging.getLogger('DaemonLog')
logger.setLevel(logging.INFO)
formatter = logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s")
handler = logging.FileHandler('/var/log/amrusb/amrusb.log')
handler.setFormatter(formatter)
logger.addHandler(handler)

app.run()
