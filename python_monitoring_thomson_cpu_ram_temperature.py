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

# Check for required options
for option in ('host', 'community'):
    if not getattr(options, option):
        print 'Option %s not specified' % option
        parser.print_help()
        sys.exit(UNKNOWN)

# OID cho 2 cpu
oid_cpu1="1.3.6.1.4.1.232.1.2.2.1.1.6.0"
oid_cpu2="1.3.6.1.4.1.232.1.2.2.1.1.6.1"
#OID cho 16 Ram
nram=16
oid1="1.3.6.1.4.1.232.6.2.14.13.1.20."
oid_ram=[]
for i in range(0,nram):
	oid_ram.append(oid1 + str(i))
str_oid_ram=''
for i in range(0,nram-1):
	str_oid_ram = str_oid_ram + oid_ram[i] + ","
str_oid_ram += oid_ram[nram-1]
#OID cho 33 cam bien nhiet
ntem=33
oid2= "1.3.6.1.4.1.232.6.2.6.8.1.6.0."
oid_tem=[]
for i in range(0,ntem):
	oid_tem.append(oid2 + str(i + 1))
str_oid_tem=''
for i in range(0,ntem-1):
	str_oid_tem = str_oid_tem + oid_tem[i] + ","
str_oid_tem += oid_tem[ntem-1]

print str_oid_tem
print str_oid_ram
# Query SNMP
msg = ''
msg_cpu=''
msg_ram=''
msg_tem=''

sess = netsnmp.Session(Version = 2, DestHost = options.host, Community = options.community, Timeout=1000000, Retries=1)
vars = netsnmp.VarList(oid_cpu1,oid_cpu2)
result = sess.get(vars)
print "KQ: " + str(result)
print len(result)

status=OK
if result[0] == None:
	print 'UNKNOW: Host not responding to SNMP request'
	sys.exit(UNKNOWN)

msga=[]
for i in range(0, n1 + n2):
	if int(result[i])==1:
		msga.append("Unknown")
	elif int(result[i])==2:
		msga.append("OK")
	elif int(result[i])==3:
		msga.append("Degraded")
	elif int(result[i]) == 4:
		msga.append("Failed")
	else:
		msga.append("Disable")
		
#Chi can co 1 cai !=2 la Critical
count_cri=0
count_ok=0
for i in range(0, n1 + n2):
	if int(result[i]) <> 2:
		status=CRITICAL
		count_cri +=1
	else:
		count_ok +=1

for i in range(0, n1):
	temp="Cam bien nhiet " + str(i+1) + ":" + msga[i] + "\n  "
	msg_tem += temp 
#Doi tu n1-n2 thanh (i-n1+1)-(n2-n1+1)
for i in range(n1, n2):
	temp="Canh quat " + str(i-n1+1) + ":" + msga[i] + "\n  "
	msg_fan += temp

msg = msg_tem + msg_fan
msg_status = {0:str(count_ok) + ' OK', 1:'WARNING', 2:str(count_cri) + ' CRITICAL', 3:'UNKNOWN'} [status]	
msg = msg_status + ':\n  ' + msg

print msg
sys.exit(status)	

