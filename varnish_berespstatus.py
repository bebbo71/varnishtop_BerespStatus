#!/usr/bin/python3

#BerespStatus - Backend response status (The HTTP status code received).
#varnishtop -1 -I BerespStatus:[45]0[01234]
#Options: [-1] Run once; [-I <[taglist:]regex>] Include by regex
#Output: e.g. root@varnishserver:~# varnishtop -1 -I BerespStatus:[45]0[01234] # z.B. varnishtop -1 -I BerespStatus:\(40[0-4]\|50[0-24]\) without 503
#  9829.00 BerespStatus 401
#    15.00 BerespStatus 403
#     2.00 BerespStatus 400
#Seconds to measure over, the default is 60 seconds. The first number in the list is the average number of requests seen over this time period.
#Output is reset to 0 when the Varnish service is restarted.
#Script under '/opt/app/check-mk-agent/lib/local/myscript' take off and perform with 'chmod +x myscript'.

import os, sys, json

file='/tmp/varnish_berespstatus_check_mk.txt'

def writefile(dictw):
    try:
        with open(file, 'w') as f:
            json.dump(dictw, f)
    except:
        sys.exit(0)

#Prepare a file to secure the queried requests
dictStart = {'400': 0.0, '401': 0.0, '402': 0.0, '403': 0.0, '404': 0.0, '500': 0.0, '501': 0.0, '502': 0.0, '503': 0.0, '504': 0.0}
if not os.path.isfile(file):
    writefile(dictStart)

#Query the average requests of the last 60 seconds
try:
    varnishtopOut = os.popen('varnishtop -1 -I BerespStatus:[45]0[01234]','r')
except:
    sys.exit(0)
    
#convert varnishtopOut output to a dictionary {'404': 2.0, '401': 10517.0, '403': 15.0, '400': 2.0}
#Output is reset only when restarting the Varnish service and returns empty string.
count = 1
abbruch = False
while not(abbruch):
    lines = varnishtopOut.readlines()
    if not lines and count == 1:
        print('0 varnish_backend_response_status 400=0|401=0|402=0|403=0|404=0|500=0|501=0|502=0|503=0|504=0 OK - Es treten keine HTTP Fehler auf')
        writefile(dictStart)
        sys.exit(0)
    if not lines: break
    count +=1
    stripLine = [i.strip() for i in lines]
    line = []
    for i in range(len(stripLine)):
        line.append(stripLine[i].split())
    zwListe = []
    for i in range(len(line)):
        zwListe.append(line[i][2] + ":" + line[i][0])
    dict = {k:float(v) for k,v in (x.split(':') for x in zwListe)}
abbruch = True

#Dictionary read file
try:
    with open(file) as f:
        dictOutFile = json.load(f)
except:
    sys.exit(0)

#Query requests with cached compare and edit and prepare for Check_mk
status = 0
statustxt = 'OK'
output = 'Es treten keine HTTP Fehler auf'
zwString = ''
for k, v in dictOutFile.items():
    if k not in dict:
        zwString += (k+'='+str('0')+'|')
        continue
    if v > dict[k]:
        zwString += (k+'='+str('0')+'|')
    if v == dict[k]:
        zwString += (k+'='+str('0')+'|')
    if v < dict[k]:
        zwString += (k+'='+str(dict[k])+'|')
        status = 1
        statustxt = 'WARNING'
        output = 'Es treten HTTP Fehler auf'
dictOutFile.update(dict)

ausgabeString = zwString.rstrip('|')
ausgabeListe = ausgabeString.split('|')
ausgabeListe.sort()
varnishBerespstatus = ("|".join(map(str, ausgabeListe)))
print(status, 'varnish_backend_response_status', varnishBerespstatus, statustxt, '-', output)

#Save the edited dictionary again
writefile(dictOutFile)
