#!/usr/bin/env python

import sys
import csv
import time
import datetime

import boto
from boto.dynamodb2.table import Table

electric_meter_serial = 57521019
water_meter_serial = 30142394

readings = Table('readings')

result_set = readings.query_2(
    serialnumber__eq = water_meter_serial,
    datestamp__gte = time.time() - (24 * 60 * 60),
    limit = 1
)

for reading in result_set:
    print str(reading['serialnumber']) + ',' + datetime.datetime.fromtimestamp(reading['datestamp']).strftime('%Y-%m-%d %H:%M:%S') + ',' + str(reading['reading']) + ',' + str(reading['type'])

result_set = readings.query_2(
    serialnumber__eq = water_meter_serial,
    datestamp__gte = time.time() - (24 * 60 * 60),
    limit = 1,
    reverse=True,
)

for reading in result_set:
    print str(reading['serialnumber']) + ',' + datetime.datetime.fromtimestamp(reading['datestamp']).strftime('%Y-%m-%d %H:%M:%S') + ',' + str(reading['reading']) + ',' + str(reading['type'])

