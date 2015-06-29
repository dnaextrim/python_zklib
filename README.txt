# Python ZKLib #

Attendance Machine Library for python with a connection to the network using the UDP protocol and port 4370

## Getting started

Login as admin to attendance machine and set the ip address for example (to 192.168.0.201) and connect the machine with ethernet to your network.
```bash
pip install zklib
```
Connect to the machine

```python
import sys
import zklib
import time
import zkconst

zk = zklib.ZKLib("192.168.0.201", 4370)
ret = zk.connect()
print "connection:", ret
```

If result was
```
connection True
```
Then you are connected.

More examples on how to use the Library available in the
zktest.py file
