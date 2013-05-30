#! /usr/local/bin/python
# For user-specified zip codes, queries the transit API for public transit info (intra-city only)

import numpy
from urllib import urlopen
from json import load
import time
import datetime

# Libraries for hashing the private key
import sys
import hashlib
import urllib
import hmac
import base64
import urlparse

# Defines the arrival time as the first monday following the day the program is run, 
# at 8 am, and converts to unix time

wkdy = datetime.date.today().weekday()
monday = datetime.date.today() + datetime.timedelta(days=7-wkdy)
arrivetime = datetime.time(8,0,0)
arrivedate = datetime.datetime.combine(monday,arrivetime).timetuple()
roundtime = int(time.mktime(arrivedate))

END_ADDRESS = raw_input('Destination address (no spaces!):')


def urlSigner(rawURL):

    url = urlparse.urlparse(rawURL+'&client=gme-cushmanwakefield&channel=CFIB')

    privateKey = ''

    # Sign the path+query part of the string
    urlToSign = url.path + "?" + url.query

    # Decode the private key into its binary format
    decodedKey = base64.urlsafe_b64decode(privateKey)

    # Create a binary signature using the private key and the URL-encoded
    # string using HMAC SHA1. 
    signature = hmac.new(decodedKey, urlToSign, hashlib.sha1)

    # Encode the binary signature into base64 for use within a URL
    encodedSignature = base64.urlsafe_b64encode(signature.digest())
    originalUrl = url.scheme + "://" + url.netloc + url.path + "?" + url.query
    urlToPass = (originalUrl + "&signature=" + encodedSignature)

    return urlToPass


def getInfo(startzip, destination):
   # String together the URL using the individual start location, the central
   # destination, and the time

    baseURL = ('http://maps.googleapis.com/maps/api/directions/'
    'json?origin=%s&destination=%s&sensor=false&departure_time'
    '=%s&mode=transit' % (startzip, END_ADDRESS, roundtime))

    # Hash the URL using HMAC function defined above

    signedURL = urlSigner(baseURL)
    response = load(urlopen(signedURL))
    status = response['status']
        
    if status == 'OK':

        result = response['routes'][0]['legs'][0]
        duration_seconds = result['duration']['value']
        duration_minutes = duration_seconds / 60
        address = result['start_address']

        return duration_minutes, address
       
    else: 
        return status, 'none'

results = []
#ziplist = numpy.genfromtxt('C:\Users\mquaintance\Desktop'
    #'\zips.txt', dtype=str)
ziplist = ['06811','08691','10025']

for i in ziplist:
    duration, address = getInfo(i, END_ADDRESS)
    print i, duration, address
    results.append([i, duration, address])

numpy.savetxt('transit-%s.csv' % END_ADDRESS, results, fmt='%s', delimiter=",")
