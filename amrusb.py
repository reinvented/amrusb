#!/usr/bin/env python

import serial
import logging
import time
from time import strftime
import boto
from boto.dynamodb2.table import Table

class App():

    def __init__(self):
        self.device = '/dev/ttyACM0'

    def run(self):
        logger.info('Starting amrusb daemon')
        logger.info('Opening device ' + self.device)
        logger.info('Connected to Amazon Dynamo DB')
        readings = Table('readings')
        ser = serial.Serial(self.device)
        while True:
            line = ser.readline().rstrip()
            logger.info(line)
            amrvalues = line.split(',')
            if (amrvalues[0] == '$UMSCM'):
                readingvalue = amrvalues[3].split('*');
                readings.put_item(data={'serialnumber': int(amrvalues[1]), 'datestamp': int(time.time()), 'reading': int(readingvalue[0]), 'type': int(amrvalues[2])})

app = App()

logger = logging.getLogger('DaemonLog')
logger.setLevel(logging.INFO)
formatter = logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s")
handler = logging.FileHandler('/var/log/amrusb/amrusb.log')
handler.setFormatter(formatter)
logger.addHandler(handler)

app.run()