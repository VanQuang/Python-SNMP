#!/usr/bin/python
from optparse import OptionParser
import MySQLdb
import sys

# Exit statuses recognized by Nagios
OK = 0
WARNING = 1
CRITICAL = 2
UNKNOWN = 3
msg=''

# Parsing argurments
parser = OptionParser()
parser.add_option("-H", dest="host", type="string",
                  help="Hostname/IP Address of device", metavar=' ')
parser.add_option("-u", "-U", dest="user", type="string",
                  help="User of MySQL", metavar=' ')
parser.add_option("-p", "-P", dest="password", type="string",
                  help="Password of MySQL", metavar=' ')
(options, args) = parser.parse_args()

# Check for required options
for option in ('host', 'user','password'):
    if not getattr(options, option):
        print 'Option %s not specified' % option
        parser.print_help()
        sys.exit(UNKNOWN)

try:
	con = MySQLdb.connect(host=options.host,user=options.user, passwd=options.password, db="monitor")
	cur = con.cursor() 
	
	sql="SELECT al.id,ag.name as agent_name,al.input_card,al.date_time,ch.name as channel_name,pr.type,pr.ip as profile_ip,al.msg FROM channel as ch,profile as pr,agent as ag,alarm as al WHERE ch.id=pr.channel_id and pr.id=al.source_id and ag.id=al.agent_id and msg not like '%0.00%' and flag='0'"

	cur.execute(sql)
	count=cur.rowcount
	if count==0:
		msg='All channel OK'
		status=OK
	else:	
		for row in cur.fetchall():
			line=row[1] + ' ' + row[2] + " " + row[4] + ' ' + row[5] + ' ' + row[6] + ' '+ row[7] + ' '+ str(row[3]) + '\n'
			msg += line
			status=CRITICAL
	
	cur.close()
	con.close()
except MySQLdb.Error, e:
	try:
	        msg = "MySQL Error [%d]: %s" % (e.args[0], e.args[1])
	except IndexError:
        	msg = "MySQL Error: %s" % str(e)
	status=CRITICAL

msg_status = {0:'OK', 1:'WARNING', 2:'CRITICAL', 3:'UNKNOWN'} [status]	
msg= msg_status + ':\n' + msg
print msg
sys.exit(status)
