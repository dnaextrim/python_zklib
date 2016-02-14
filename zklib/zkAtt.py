from struct import pack, unpack
from datetime import datetime, date
import sys

from zkconst import *



def reverseHex(hexstr):
    tmp = ''
    for i in reversed( xrange( len(hexstr)/2 ) ):
        tmp += hexstr[i*2:(i*2)+2]
    
    return tmp


def zkAtt(self):

	
    
	command = CMD_ATTLOG_RRQ
	comand_string = ''
	chksum = 0
	session_id = self.session_id
	reply_id = unpack('4H',self.data_recv[:8])[3]

	buf = self.createHeader(command,chksum,session_id, reply_id, comand_string)
	self.zkclient.sendto(buf,self.address)
   

	attendance = []  
	self.data_recv, addr = self.zkclient.recvfrom(1024)


	if unpack('4H',self.data_recv[:8])[0] == CMD_PREPARE_DATA:
		print "received CMD_PREPARE_DATA"

		while unpack('4H', self.data_recv[:8])[0] != 2000:

			data_recv, addr = self.zkclient.recvfrom(1024)
		
			self.attendancedata.append(data_recv)
			
			if unpack('4H', data_recv[:8])[0] == 1501:
				print "receiving Data packet"
				

			self.data_recv, addr = self.zkclient.recvfrom(1024)
		
			if unpack('4H', self.data_recv)[0] == 2000:
				print "received CMD_ACK_OK"
				try:

					self.data_recv, addr = self.zkclient.recvfrom(1024)
					
				except:
					print "socket timeout - no more data to receive"
				

					for x in xrange(len(self.attendancedata)):
					
						self.attendancedata[x] = self.attendancedata[x][0:]


					attendancedata = self.attendancedata



					attendancedata = ''.join( self.attendancedata)
            
            		attendancedata = attendancedata[14:]
            		
            		while len(attendancedata):

            			
            		
            			pls = unpack('c',attendancedata[29:30])#[3]
            		
            		



            			uid, state, timestamp, space = unpack( '24s1s4s11s', attendancedata.ljust(40)[:40] )
            			#print "%s, %s, %s, %s" % (uid, ord(pls[0]), ord(space[0]), decode_time( int( reverseHex( timestamp.encode('hex') ), 16 ) ) )
            			
            			attendance.append( ( uid, ord(pls[0]), decode_time( int( reverseHex( timestamp.encode('hex') ), 16 ) ) ) )
            			attendancedata = attendancedata[40:]
            			
            	return attendance







def zkclearattendance(self):
    """Start a connection with the time clock"""
    command = CMD_CLEAR_ATTLOG
    command_string = ''
    chksum = 0
    session_id = self.session_id
    reply_id = unpack('HHHH', self.data_recv[:8])[3]

    buf = self.createHeader(command, chksum, session_id,
        reply_id, command_string)
    self.zkclient.sendto(buf, self.address)
    #print buf.encode("hex")
    try:
        self.data_recv, addr = self.zkclient.recvfrom(1024)
        self.session_id = unpack('HHHH', self.data_recv[:8])[2]
        return self.data_recv[8:]
    except:
        return False
