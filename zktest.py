import sys
sys.path.append("zklib")

import zklib

zk = zklib.ZKLib("192.168.1.201", 4370)

print "Pesan Koneksi:", zk.connect()
"""
print "Pesan Versi:", zk.version()
print "Pesan Versi OS:", zk.osversion()
print "Pesan Extend Format:", zk.extendFormat()
print "Pesan Extend OP Log:", zk.extendOPLog()
print "Pesan Platform:", zk.platform()
"""
