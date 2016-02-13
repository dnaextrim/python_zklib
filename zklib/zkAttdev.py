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

	print "testing"
	file = open("binw", "w")
    
	command = CMD_ATTLOG_RRQ
	comand_string = ''
	chksum = 0
	session_id = self.session_id
	reply_id = unpack('4H',self.data_recv[:8])[3]

	buf = self.createHeader(command,chksum,session_id, reply_id, comand_string)
	self.zkclient.sendto(buf,self.address)
    #file.write(self.data_recv[0:])
    #print "reply_id", reply_id

	attendance = []  
	self.data_recv, addr = self.zkclient.recvfrom(1024)
	#print "unpack HcHc :7", unpack('HcHc',self.data_recv[:7])
	#print "unpack HHHH :8", unpack('HHHH',self.data_recv[:8])
	#print "unpack HHHH :8 [1]", unpack('4H',self.data_recv[:8])[0]
	#print "length", len(self.data_recv)
	#print "unpack 4I  ", unpack ('4I', self.data_recv)
	#print "unpack 8H", unpack('8H', self.data_recv)
	#print "unpack I 8:12 [0]", unpack ('I', self.data_recv[8:12])[0]

	if unpack('4H',self.data_recv[:8])[0] == CMD_PREPARE_DATA:
		print "received CMD_PREPARE_DATA"

		while unpack('4H', self.data_recv[:8])[0] != 2000:

			data_recv, addr = self.zkclient.recvfrom(1024)
			#print "length of reiceived data packet", len(data_recv)
			#print "unpack 126H", unpack('126H', data_recv)
			self.attendancedata.append(data_recv)
			file.write(data_recv)
			if unpack('4H', data_recv[:8])[0] == 1501:
				print "receiving Data packet"
				#print "trying to unpack data", unpack('i', data_recv[:8])[1]

			self.data_recv, addr = self.zkclient.recvfrom(1024)
			#print "length of reiceived data packet", len(self.data_recv)
			#print unpack('4H', self.data_recv)
			if unpack('4H', self.data_recv)[0] == 2000:
				print "received CMD_ACK_OK"
				try:

					self.data_recv, addr = self.zkclient.recvfrom(1024)
					#print len(self.data_recv)
				except:
					print "socket timeout - no more data to receive"
					#print "length of att data", len(self.attendancedata)

					for x in xrange(len(self.attendancedata)):
						#print self.attendancedata[x][8:]
						#self.attendancedata[x] = self.attendancedata[x][8:]
						#print self.attendancedata[x][0:]
						self.attendancedata[x] = self.attendancedata[x][0:]


					attendancedata = self.attendancedata



					attendancedata = ''.join( self.attendancedata)
            
            		attendancedata = attendancedata[14:]
            		
            		while len(attendancedata):

            			#print "length att", len(attendancedata)
            			uidm = unpack('24s1s4s11s',attendancedata.ljust(40)[:40])
            			#print "length att40", len(attendancedata[:38])
            			uidt = unpack('38s',attendancedata[:38])
            			#print "uidt", uidt
            			#print "sizeof", sys.getsizeof(attendancedata[:40])
            			#try unpacking the state bits in reverse order
            			#try unpacking using different endianness
            			#timestamp = int.from_bytes(ba_object[:4], byteorder='big')
            			#print "LENNY", len(attendancedata[30:])
            			uidmn = unpack('16s',attendancedata[:16])[0]
            			pls = unpack('c',attendancedata[29:30])#[3]
            			#print "pls wo ord", pls
            			#statem = unpack('=5c',attendancedata[:10])[3]
            			statev = unpack('=2c',attendancedata[21:23])
            			datem = unpack('ii',attendancedata[:8])[1]
            			#print "uidm", uidm
            			#print "uidmn", uidmn
            			#print "pls w ord", ord(pls[0])
            			#print "statem", ord(statem)
            			#print "statev", ord(statev[0])
            			#print "statev", statev[0]
            			#print "datem",datem



            			uid, state, timestamp, space = unpack( '24s1s4s11s', attendancedata.ljust(40)[:40] )
            			print "%s, %s, %s, %s" % (uid, ord(pls[0]), ord(space[0]), decode_time( int( reverseHex( timestamp.encode('hex') ), 16 ) ) )
            			#print "%s, %s, %s, %s" % (uid, state, space, timestamp)
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