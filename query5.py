#! /usr/local/bin/python
#for user-specified zip codes, queries the transit API for public transit info (intra-city only)


import numpy
ziplist = numpy.genfromtxt('C:\Users\mquaintance\Desktop'
    '\zips.txt', dtype=str)
#ziplist = ['06811','08691']

import json
import urllib
from time import time
roundtime=int(time())

b=raw_input('Destination zip:')

def getInfo(startzip,destination):

    status = []
    
    url = ('http://maps.googleapis.com/maps/api/directions/'
    'json?origin=%s&destination=%s&sensor=false&departure_time'
    '=%s&mode=transit' % (startzip,destination,roundtime))
    #print url
    response = json.load(urllib.urlopen(url))
    status = (response['status'])
    
    while status == "OVER_QUERY_LIMIT": 
        print status
        import time
        time.sleep(5)
        url = ('http://maps.googleapis.com/maps/api/directions/'
        'json?origin=%s&destination=%s&sensor=false&departure_time'
        '=%s&mode=transit' % (startzip,destination,roundtime))
        #print url
        response = json.load(urllib.urlopen(url))
        status = (response['status'])
   
    if status == "ZERO_RESULTS":
        return status, status
    else:

        duration = (response['routes'][0]['legs'][0]['duration']['value'])
        address = (response['routes'][0]['legs'][0]['start_address'])
        return duration/60, address

x = []
results = []
dur=[]
add=[]

for x  in ziplist:
    dur,add = getInfo(x, b)
    print x,dur,add
    results.append([x,dur,add])

numpy.savetxt('transit'+'%s''.csv' % (b),results,fmt='%s',delimiter=",")

