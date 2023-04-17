from getloc import *
from scapy.all import *


def test_path(hostname):
    available_path = []    
    for i in range(1, 28):
        pkt = IP(dst=hostname, ttl=i) / UDP(dport=33434)    
        reply = sr1(pkt, verbose=0, timeout=.1)    
        if reply is None:
            # print("problem with hop ", i)
            pass
        elif reply.type == 3:
            available_path.append(reply.src)
            # print("Done!", reply.src)
            
            break            
        else:
            print("%d hops away: " % i, reply.src, reply.time)
            available_path.append(reply.src)
    return available_path



if __name__ == "__main__":
    test_path("8.8.8.8")