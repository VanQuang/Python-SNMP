#!/usr/bin/python
from optparse import OptionParser
import netsnmp
import sys
import string
import time

# Exit statuses recognized by Nagios
start_time = time.time()
OK = 0
WARNING = 1
CRITICAL = 2
UNKNOWN = 3

# Parsing argurments
parser = OptionParser()
parser.add_option("-H", dest="host", type="string",
                  help="Hostname/IP Address of device", metavar=' ')

parser.add_option("-c", "-C", dest="community", type="string",
                  help="Community string", metavar=' ')

(options, args) = parser.parse_args()

# OID
#oid_test=".1.3.6.1.4.1.1238.1.1.101.1"
oid_tem= ".1.3.6.1.4.1.232.22.2.3.1.2.1.8.60"
oid_fan= ".1.3.6.1.4.1.232.22.2.3.1.3.1.11.10"
# Query SNMP
msg = ''
# Check for required options
for option in ('host', 'community'):
    if not getattr(options, option):
        print 'Option %s not specified' % option
        parser.print_help()
        sys.exit(UNKNOWN)

sess = netsnmp.Session(Version = 2, DestHost = options.host, Community = options.community, Timeout=1000000, Retries=1)
vars = netsnmp.VarList(oid_tem,oid_fan)
result = sess.get(vars)

status=OK
if result[0] == None:
	print 'UNKNOW: Host not responding to SNMP request'
	sys.exit(UNKNOWN)
print "Result: " + str(result)

msga=[0,0]
for i in range(0, 2):
	print result[i]
	if int(result[i])==1:
		msga[i]="Unknown"
	elif int(result[i])==2:
		msga[i]="OK"
	elif int(result[i])==3:
		msga[i]="Degraded"
	else:
		msga[i]="Failed"
		
#Chi can co 1 cai !=2 la Critical
for i in range(0, 2):
	if int(result[i]) <> 2:
		status=CRITICAL
		
msg="Temperature:" + msga[0]+ " Fan:" + msga[1]
msg_status = {0:'OK', 1:'WARNING', 2:'CRITICAL', 3:'UNKNOWN'} [status]	
msg= msg_status + ':\n' + msg

print msg
sys.exit(status)	


