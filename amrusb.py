#!/usr/bin/env python

import serial
import logging
import time
import sys

from time import strftime
import boto
from boto.dynamodb2.table import Table

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
        logger.info('Connected to Amazon Dynamo DB')
        readings = Table('readings')
        ser = serial.Serial(self.device)
        while True:
            try:
                line = ser.readline().rstrip()
            except:
                logger.error(sys.exc_info()[0])
                raise
            else:
                logger.info(line)
                amrvalues = line.split(',')
                if (amrvalues[0] == '$UMSCM'):
                    readingvalue = amrvalues[3].split('*');
                    try:
                        readings.put_item(data={'serialnumber': int(amrvalues[1]), 'datestamp': int(time.time()), 'reading': int(readingvalue[0]), 'type': int(amrvalues[2])})
                    except:
                        logger.error(sys.exc_info()[0])
                        raise

app = App()
logger = logging.getLogger('DaemonLog')
logger.setLevel(logging.INFO)
formatter = logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s")
handler = logging.FileHandler('/var/log/amrusb/amrusb.log')
handler.setFormatter(formatter)
logger.addHandler(handler)

app.run()
