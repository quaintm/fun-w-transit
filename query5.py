#! /usr/local/bin/python
#for user-specified zip codes, queries the transit API for public transit info (intra-city only)

import numpy
from urllib import urlopen
from json import load
from time import time

roundtime = int(time())
END_ZIP = raw_input('Destination zip:')

def getStatus():
    url = ('http://maps.googleapis.com/maps/api/directions/'
    'json?origin=%s&destination=%s&sensor=false&departure_time'
    '=%s&mode=transit' % (startzip, END_ZIP, roundtime))
    response = load(urlopen(url))
    return response.status

def getInfo(startzip, destination):
    
    while status == "OVER_QUERY_LIMIT": 
        print status
        time.sleep(5)
        status = getStatus()
   
    hasResult = (status != 'ZERO_RESULTS')
    if hasResult:
    	result = response['routes'][0]['legs'][0]
    	duration_minutes = result.duration.value
    	duration_hours = duration_minutes / 60
    	address = result.start_address
    else:
    	duration_hours, address = status, status

    return duration_hours, address

results = []
ziplist = numpy.genfromtxt('C:\Users\mquaintance\Desktop'
    '\zips.txt', dtype=str)

for i in ziplist:
    duration, address = getInfo(x, zip)
    print i, duration, address
    results.append([i, duration, address])

numpy.savetxt('transit' + '%s.csv' % END_ZIP, results, fmt='%s', delimiter=",")
