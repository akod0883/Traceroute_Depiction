import argparse
import ipaddress
import socket
import sys

import icmplib

from getloc import *
from help import *
from plot import *
from test_path import *

# get hostname from parse
if len(sys.argv)<3:
    printHelp()
    exit()
    

parser = argparse.ArgumentParser()

# Add the protocol_type argument as a mandatory option
parser.add_argument("protocol_type", choices=["udp", "icmp"], help="The protocol type (udp or icmp)")

# Add the hostname argument
parser.add_argument("hostname", help="The hostname")

# Parse the command line arguments
args = parser.parse_args()

# Get the protocol_type and hostname arguments
traceroute_type = args.protocol_type
hostname = args.hostname



# hostname = sys.argv[1]
# traceroute_type = sys.argv[2]
targetIP = ""
# hostname = "ox.ac.uk"

# if hostname provided is an ip address, check its validity
if hostname[0].isdigit():
   ipaddress.ip_address(hostname)
   targetIP = hostname
else:
    targetIP = socket.gethostbyname(hostname)

# get my location (myIP,(lon,lat),city)
myLoc = getMyLoc()
print("starting location ", myLoc)

# get target location IP,(lon,lat),city
targetLoc = getTargetLoc(targetIP)
print("target location ", targetLoc)

ipList = []

if traceroute_type == "udp":
    ipList = test_path(targetIP)
else:
    ipObjectList = icmplib.traceroute(targetIP, timeout=.1)
    for ip_object in ipObjectList:        
        ipList.append(ip_object.address)

if ipList[-1] != targetIP:
    print("traceroute to destination could not be found")
    print("printing longest resolved path")


# get geo location of the ipList and insert myLoc and TargetLoc
routeLocList = getLoc(ipList)

routeLocList.insert(0,myLoc)
routeLocList.append(targetLoc)

print("path to destination")
for route in routeLocList:
    print(route)

# prepare for and linear route in map
routeLocLon =[]
routeLocLat = []
tempLon = 0
tempLat = 0

for x in routeLocList:
    # this looping will drop the route that have zero movement
    if x[1][0]-tempLon == 0 or x[1][1]-tempLat == 0:
        continue
    routeLocLon.append(x[1][0])
    routeLocLat.append(x[1][1])

    tempLon = x[1][0]
    tempLat = x[1][1]


# initiate the maps
fig = go.Figure()
mapsInit(fig)

# creating the route
for i in range(len(routeLocLon)-1):
    for x in routeLocList:
        if (routeLocLon[i],routeLocLat[i]) in x:
            route_city = x[2]
            route_ip = x[0]
    print(route_ip,'---',route_city)
    addRoute(fig,f'route{i}',((routeLocLon[i:i+2],routeLocLat[i:i+2]),route_city))
print(targetLoc[0],'---',targetLoc[2])

# marking the source IP and destination IP
mark(fig,f'My IP - {myLoc[2]}', myLoc[1])
mark(fig,f'{hostname} - {targetLoc[2]}',targetLoc[1],name=hostname)

fig.show()
