import sys
sys.path.append("zklib")

import zklib
import time

zk = zklib.ZKLib("192.168.1.201", 4370)

ret = zk.connect()
print "Pesan Koneksi:", ret

if ret == True:
    print "Pesan Disable Device", zk.disableDevice()
    
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
    if data_user:
        for uid in data_user:
            if data_user[uid][1] == 14:
                level = 'Admin'
            else:
                level = 'User'
            print "ID %s: %s, Level: %s, Password: %s" % ( uid, data_user[uid][0], level, data_user[uid][2]  )
        
    #print "Pesan Clear Admin:", zk.clearAdmin()
    
    
    attendance = zk.getAttendance()
    print "Pesan Get Attendance:"
    
    if attendance:
        for lattendance in attendance:
            if lattendance[1] == 15:
                state = 'Check In'
            elif lattendance[1] == 0:
                state = 'Check Out'
            else:
                state = 'Undefined'
                
            print "Tanggal %s, Jam %s: %s, Status: %s" % ( lattendance[2].date(), lattendance[2].time(), lattendance[0], state )
        
        print "Pesan Clear Attendance:", zk.clearAttendance()
    
    print "Pesan Get Time:", zk.getTime()
    
    print "Pesan Enable Device", zk.enableDevice()
    
    print "Pesan Disconnect:", zk.disconnect()
