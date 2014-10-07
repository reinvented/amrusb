#!/usr/bin/env python

import sys
import csv

import boto
from boto.dynamodb2.table import Table

readings = Table('readings')

result_set = readings.scan()
for reading in result_set:
    print str(reading['serialnumber']) + ',' + str(reading['datestamp']) + ',' + str(reading['reading']) + ',' + str(reading['type'])

