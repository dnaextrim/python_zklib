from struct import pack, unpack
from datetime import datetime, date
import sys

from zkconst import *


def acmOK(self):
    """send CMD_ACK_OK"""
    """ try cmd_ack_data"""
    command = CMD_ACK_DATA
    command_string = ''
    chksum = 0
    session_id = 0
    reply_id = -1 + USHRT_MAX

    buf = self.createHeader(command, chksum, session_id,
                            reply_id, command_string)

    self.zkclient.sendto(buf, self.address)

    try:
        self.data_recv, addr = self.zkclient.recvfrom(1024)
        self.session_id = unpack('HHHH', self.data_recv[:8])[2]

        return self.checkValid(self.data_recv)
    except:
        return False


def reverseHex(hexstr):
    tmp = ''
    for i in reversed(xrange(len(hexstr) / 2)):
        tmp += hexstr[i * 2:(i * 2) + 2]

    return tmp


def zkAtt(self):

    command = CMD_ATTLOG_RRQ
    comand_string = ''
    chksum = 0
    session_id = self.session_id
    reply_id = unpack('4H', self.data_recv[:8])[3]

    buf = self.createHeader(command, chksum, session_id,
                            reply_id, comand_string)
    self.zkclient.sendto(buf, self.address)

    size = None
    attendance = []
    self.data_recv, addr = self.zkclient.recvfrom(1024)
    # print unpack('24s1s4s11s',self.data_recv.ljust(40)[:40])
    # print "unpack HcHc :7", unpack('HcHc',self.data_recv[:7])
    # print "unpack HHHH :8", unpack('HHHH',self.data_recv[:8])
    # print "unpack HHHH :8 [1]", unpack('4H',self.data_recv[:8])[0]
    print "size", sys.getsizeof(self.data_recv)
    print "size", len(self.data_recv)
    lensi = len(self.data_recv) / 2
    fstri = str(lensi) + "H"
    print "unpack 4I  ", unpack(fstri, self.data_recv)
    # print "unpack 8H", unpack('8H', self.data_recv)
    # print "unpack I 8:12 [0]", unpack ('I', self.data_recv[8:12])[0]

    attendance = []
    self.data_recv, addr = self.zkclient.recvfrom(1024)

    if unpack('4H', self.data_recv[:8])[0] == CMD_PREPARE_DATA:
        print "received CMD_PREPARE_DATA"
        size = unpack('I', self.data_recv[8:12])[0]

        wa = unpack('II', self.data_recv[:8])[0]
        print "received ", wa
        print 'Receiving %s %s' % (size, "bytes")
        try:

            data_recv, addr = self.zkclient.recvfrom(size)
            print "size of data_recv", sys.getsizeof(data_recv)
            self.attendancedata.append(data_recv)
            acmOK(self)
            print unpack('24s1s4s11s', self.data_recv.ljust(40)[:40])

        except:

            print "socket timeout 1 - no more data to receive"

        while unpack('4H', self.data_recv[:8])[0] != 2000 or unpack('4H', self.data_recv[:8])[0] == 1501:

            try:

                data_recv, addr = self.zkclient.recvfrom(size)
                acmOK(self)
                print unpack('24s1s4s11s', self.data_recv.ljust(40)[:40])

            except:

                print "socket timeout 2 - no more data to receive"
                self.attendancedata.append(data_recv)
                acmOK(self)
                break
            # print "length of reiceived data packet", len(data_recv)
            # print "unpack 126H", unpack('126H', data_recv)

            data_recv, addr = self.zkclient.recvfrom(1024)

            self.attendancedata.append(data_recv)

            if unpack('4H', self.data_recv[:8])[0] == CMD_PREPARE_DATA:

                print "received CMD_PREPARE_DATA"
                size = unpack('I', self.data_recv[8:12])[0]
                print 'Receiving %s %s' % (size, "bytes")

            elif unpack('4H', data_recv[:8])[0] == 1501:
                print "receiving Data packet"

            elif unpack('4H', self.data_recv[:8])[0] == 2000:
                print "received CMD_ACK_OK"
                try:

                    self.data_recv, addr = self.zkclient.recvfrom(size)
                    acmOK(self)
                    # print len(self.data_recv)
                except:
                    print "socket timeout 3 - no more data to receive"

            #self.data_recv, addr = self.zkclient.recvfrom(1024)
            # print "length of reiceived data packet", len(self.data_recv)
            print "length", len(self.data_recv)
            lens = len(self.data_recv) / 2
            fstr = str(lens) + "H"

            print unpack(fstr, self.data_recv)
            if unpack('4H', self.data_recv[:8])[0] == 2000:
                print "received CMD_ACK_OK"
                try:

                    self.data_recv, addr = self.zkclient.recvfrom(4096)
                    # print len(self.data_recv)
                except:
                    print "socket timeout 4 - no more data to receive"
        print "length of att data", len(self.attendancedata)
        #data_recv = self.zkclient.recvfrom(8)

        for x in xrange(len(self.attendancedata)):

                                        # print self.attendancedata[x][8:]
                                        #self.attendancedata[x] = self.attendancedata[x][8:]
                                        # print self.attendancedata[x][0:]
            self.attendancedata[x] = self.attendancedata[x][0:]

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

        attendancedata = self.attendancedata

        attendancedata = ''.join(self.attendancedata)

        attendancedata = attendancedata[14:]
        #attendancedata = attendancedata[14:]

        print "len attendancedata", len(attendancedata)

    while len(attendancedata):

        #uidm = unpack('24s1s4s11s',attendancedata.ljust(40)[:40])

        #uidt = unpack('38s',attendancedata[:38])

        #uidmn = unpack('16s',attendancedata[:16])[0]

        pls = unpack('c', attendancedata[29:30])  # [3]

        #statev = unpack('=2c',attendancedata[21:23])
        #datem = unpack('ii',attendancedata[:8])[1]

        uid, state, timestamp, space = unpack(
            '24s1s4s11s', attendancedata.ljust(40)[:40])
        print "%s, %s, %s, %s" % (uid, 1, ord(space[0]), decode_time(int(reverseHex(timestamp.encode('hex')), 16)))
        # print "%s, %s, %s, %s" % (uid, ord(pls[0]), ord(space[0]), decode_time( int( reverseHex( timestamp.encode('hex') ), 16 ) ) )
        # print "%s, %s, %s, %s" % (uid, state, space, timestamp)
        #attendance.append( ( uid, ord(pls[0]), decode_time( int( reverseHex( timestamp.encode('hex') ), 16 ) ) ) )
        attendance.append((uid, ord(pls[0]), decode_time(
            int(reverseHex(timestamp.encode('hex')), 16))))
        attendancedata = attendancedata[40:]

        while len(attendancedata):

            pls = unpack('c', attendancedata[29:30])  # [3]

            uid, state, timestamp, space = unpack(
                '24s1s4s11s', attendancedata.ljust(40)[:40])
            # print "%s, %s, %s, %s" % (uid, ord(pls[0]), ord(space[0]),
            # decode_time( int( reverseHex( timestamp.encode('hex') ), 16 )
            # ) )

            attendance.append((uid, ord(pls[0]), decode_time(
                int(reverseHex(timestamp.encode('hex')), 16))))
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
    # print buf.encode("hex")
    try:
        self.data_recv, addr = self.zkclient.recvfrom(1024)
        self.session_id = unpack('HHHH', self.data_recv[:8])[2]
        return self.data_recv[8:]
    except:
        return False
