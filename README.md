# varnishtop_BerespStatus
#Backend response status for check_mk-agent
#tested with Ubuntu 16.04.5 LTS (Xenial Xerus) and varnish-4.1.10
#python3 script

#BerespStatus - Backend response status (The HTTP status code received).
#varnishtop -1 -I BerespStatus:[45]0[01234]
#Options: [-1] Run once; [-I <[taglist:]regex>] Include by regex
#Output: e.g. root@varnishserver:~# varnishtop -1 -I BerespStatus:[45]0[01234] # z.B. varnishtop -1 -I BerespStatus:\(40[0-4]\|50[0-24]\) ohne 503
#  9829.00 BerespStatus 401
#    15.00 BerespStatus 403
#     2.00 BerespStatus 400
#Seconds to measure over, the default is 60 seconds. The first number in the list is the average number of requests seen over this time period.
#Output is reset to 0 when the Varnish service is restarted.
#script under '/opt/app/check-mk-agent/lib/local/myscript' take off and perform with 'chmod + x'.
