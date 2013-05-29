#! /usr/local/bin/python
#for user-specified zip codes, queries the transit API for public transit info (intra-city only)

import numpy
from urllib import urlopen
from json import load
from time import time
import datetime

#defines the arrival time as the first monday following the day the program is run, 
#at 8 am, and converts to unix time

wkdy = datetime.date.today().weekday()
monday = datetime.date.today() + datetime.timedelta(days=7-wkdy)
arrivetime = datetime.time(8,0,0)
arrivedate = datetime.datetime.combine(monday,arrivetime).timetuple()
roundtime = int(time.mktime(arrivedate))

END_ZIP = raw_input('Destination zip:')

def getStatus(startzip, destination, roundtime):
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
    	duration_seconds = result.duration.value
    	duration_minutes = duration_seconds / 60
    	address = result.start_address
    else:
    	duration_minutes, address = status, status

    return duration_hours, address

results = []
#ziplist = numpy.genfromtxt('C:\Users\mquaintance\Desktop'
    #'\zips.txt', dtype=str)
ziplist = ['06811','08691','10025']

for i in ziplist:
    duration, address = getInfo(i, END_ZIP)
    print i, duration, address
    results.append([i, duration, address])

numpy.savetxt('transit' + '%s.csv' % END_ZIP, results, fmt='%s', delimiter=",")
