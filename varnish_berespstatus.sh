#!/bin/bash

#BerespStatus - Backend response status (The HTTP status code received).
#varnishtop -1 -I BerespStatus:503
#Options: [-1] Run once; [-I <[taglist:]regex>] Include by regex
#Output: e.g. 119.00 BerespStatus 503
#Output wird nur bei restart des Varnish service auf 0 zurueckgesetzt.
#script unter /opt/app/check-mk-agent/lib/local/myscript ablegen

file=/tmp/varnish_berespstatus_check_mk.txt

if [ ! -e "$file" ] ; then
	touch $file
fi

BERESPSTATUS=$(varnishtop -1 -I BerespStatus:503 | tr -s " " | cut -d" " -f2)
BERESPSTATUS_FILE=$(cat $file)

if [ -z "$BERESPSTATUS" ] ; then
	status=0
	statustxt=OK
	output="Es treten keine HTTP 503 Fehler auf"
	perfdata="fehler=0"
elif [ $(echo "if (${BERESPSTATUS_FILE} == ${BERESPSTATUS}) 1 else 0" | bc) -eq 1 ] ; then
	status=0
	statustxt=OK
	output="Es treten keine HTTP 503 Fehler auf"
	perfdata="fehler=0"
elif [ $(echo "if (${BERESPSTATUS_FILE} < ${BERESPSTATUS}) 1 else 0" | bc) -eq 1 ] ; then
	status=1
	statustxt=WARNING
	output="Es treten HTTP 503 Fehler auf"
	perfdata="fehler=${BERESPSTATUS}"
else
	status=3
	statustxt=UNKNOWN
	output="HTTP Status unbekannt"
	perfdata="fehler=0"
fi
echo "$status varnish_backend_response_status $perfdata $statustxt - $output"

echo "$BERESPSTATUS" > $file
