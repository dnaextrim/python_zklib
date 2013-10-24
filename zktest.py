import sys
sys.path.append("zklib")

import zklib

zk = zklib.ZKLib("192.168.1.201", 4370)

ret = zk.connect()
print "Pesan Koneksi:", ret

if ret == True:
    print "Pesan Versi:", zk.version()
    print "Pesan Versi OS:", zk.osversion()
    """
    print "Pesan Extend Format:", zk.extendFormat()
    print "Pesan Extend OP Log:", zk.extendOPLog()
    """
    
    print "Pesan Platform:", zk.platform()
    print "Pesan Platform Version:", zk.fmVersion()
    print "Pesan Work Code:", zk.workCode()
    print "Pesan Work Code:", zk.workCode()
    print "Pesan SSR:", zk.ssr()
    print "Pesan Pin Width:", zk.pinWidth()
    print "Pesan Face Function On:", zk.faceFunctionOn()
    print "Pesan Serial Number:", zk.serialNumber()
    print "Pesan Device Name:", zk.deviceName()
    
    data_user = zk.getUser()
    print "Pesan Get User:"
    for uid in data_user:
        print "ID %s: %s" % ( uid, data_user[uid] )
        
    print "Pesan Disconnect:", zk.disconnect()
