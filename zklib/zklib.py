from socket import *
import sys
import select
import errno
import time

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

class ZKLib:
    
    def __init__(self, ip, port):
        self.address = (ip, port)
        self.zkclient = socket(AF_INET, SOCK_DGRAM)
        self.zkclient.settimeout(3)
        self.counter = 0
        
    def connect(self):
        try:
            test = self.trynumber
        except:
            self.trynumber=1
        
        try:
            ret = zkconnect(self)
            print ret, "Koneksi"
            print self.version(), "Versi"
            print self.osversion(), "OS Versi"
            print self.extendFormat(), "Extend Format"
            print self.extendOPLog(), "Extend OP Log 0"
            print self.extendOPLog(1), "Extend OP Log 1"
            print self.extendOPLog(2), "Extend OP Log 2"
            print self.extendOPLog(3), "Extend OP Log 3"
            print self.extendOPLog(4), "Extend OP Log 4"
            print self.platform(), "Platform"
            print self.fmVersion(), "ZK Platform Version"
            print zkspace1(self), "Space 1"
            print zkworkcode(self), "Workcode"
            print zkspace2(self), "Space 2"
            print zkssr(self), "SSR"
            print zkpinwidth(self), "PIN Width"
            print zkfaceon(self), "Face Function On"
            return ret
        except:
            if self.trynumber<=5:
                print 
                print "===================="
                print "Trying Number:", self.trynumber
                print "===================="
                print
                self.trynumber = self.trynumber+1;
                self.counter = 0
                self.id_com = ""
                self.data_seq1 = ""
                self.data_seq2 = ""
                self.data_recv = ""
                time.sleep(2)
                self.connect()
            print 'recv timed out, retry later'
            sys.exit(1)
    
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
