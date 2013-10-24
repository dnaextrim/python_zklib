from socket import *
import sys
import select
import errno
import time

from struct import pack, unpack
from datetime import datetime, date

from zkconnect import *
from zkversion import *
from zkos import *
from zkextendfmt import *
from zkextendoplog import *
from zkplatform import *
from zkworkcode import *
from zkssr import *
from zkpin import *
from zkface import *
from zkserialnumber import *
from zkdevice import *
from zkuser import *

def encode_time(t):
    """Encode a timestamp send at the timeclock

    copied from zkemsdk.c - EncodeTime"""
    d = ( (t.year % 100) * 12 * 31 + ((t.month - 1) * 31) + t.day - 1) *\
         (24 * 60 * 60) + (t.hour * 60 + t.minute) * 60 + t.second

    return d


def decode_time(t):
    """Decode a timestamp retrieved from the timeclock

    copied from zkemsdk.c - DecodeTime"""
    second = t % 60
    t = t / 60

    minute = t % 60
    t = t / 60

    hour = t % 24
    t = t / 24

    day = t % 31+1
    t = t / 31

    month = t % 12+1
    t = t / 12

    year = t + 2000

    d = datetime(year, month, day, hour, minute, second)

    return d
    
    
class ZKLib:
    
    def __init__(self, ip, port):
        self.address = (ip, port)
        self.zkclient = socket(AF_INET, SOCK_DGRAM)
        self.zkclient.settimeout(3)
        self.session_id = 0
        self.userdata = []
    
    
    def createChkSum(self, p):
        """This function calculates the chksum of the packet to be sent to the 
        time clock

        Copied from zkemsdk.c"""
        l = len(p)
        chksum = 0
        while l > 1:
            chksum += unpack('H', pack('BB', p[0], p[1]))[0]
            p = p[2:]
            if chksum > USHRT_MAX:
                chksum -= USHRT_MAX
            l -= 2
        if l:
            chksum = chksum + p[-1]
        while chksum > USHRT_MAX:
            chksum -= USHRT_MAX
        chksum = ~chksum
        while chksum < 0:
            chksum += USHRT_MAX
        return pack('H', chksum)


    def createHeader(self, command, chksum, session_id, reply_id, 
                                command_string):
        """This function puts a the parts that make up a packet together and 
        packs them into a byte string"""
        buf = pack('HHHH', command, chksum,
            session_id, reply_id) + command_string
        
        buf = unpack('8B'+'%sB' % len(command_string), buf)

        chksum = unpack('H', self.createChkSum(buf))[0]
        reply_id += 1
        if reply_id >= USHRT_MAX:
            reply_id -= USHRT_MAX

        buf = pack('HHHH', command, chksum, session_id, reply_id)
        return buf + command_string
    
    
    def checkValid(self, reply):
        """Checks a returned packet to see if it returned CMD_ACK_OK,
        indicating success"""
        command = unpack('HHHH', reply[:8])[0]
        if command == CMD_ACK_OK:
            return True
        else:
            return False
            
    def connect(self):
        return zkconnect(self)
            
    def disconnect(self):
        return zkdisconnect(self)
        
    def version(self):
        return zkversion(self)
        
    def osversion(self):
        return zkos(self)
        
    def extendFormat(self):
        return zkextendfmt(self)
    
    def extendOPLog(self, index=0):
        return zkextendoplog(self, index)
    
    def platform(self):
        return zkplatform(self)
    
    def fmVersion(self):
        return zkplatformVersion(self)
        
    def workCode(self):
        return zkworkcode(self)
        
    def ssr(self):
        return zkssr(self)
    
    def pinWidth(self):
        return zkpinwidth(self)
    
    def faceFunctionOn(self):
        return zkfaceon(self)
    
    def serialNumber(self):
        return zkserialnumber(self)
    
    def deviceName(self):
        return zkdevicename(self)
    
    def getUser(self):
        return zkgetuser(self)
