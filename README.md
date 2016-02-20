# Python ZKLib #

ZK fingerprint Attendance Machine Library for python with a connection to the network using the UDP protocol and port 4370

[Donation! ![](http://i.imgur.com/2tqfhMO.png?1)](https://www.paypal.com/cgi-bin/webscr?cmd=_donations&business=DCSTC5GTWLBAN&lc=ID&item_name=donywahyuisp&currency_code=USD&bn=PP%2dDonationsBF%3abtn_donate_SM%2egif%3aNonHosted)
> sorry I could not develop this library again because I already resigned from where I work and I do not have attendance machine to develop this library
=======

## Getting started

Login as admin to attendance machine and set the ip address for example (to 192.168.0.201) and connect the machine with ethernet to your network.

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

