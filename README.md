# traceroute-maps
This project to visualize the path a packet takes from your computer to a remote domain. Also, enjoy the map generated!

There are two supported protocols in which packets can be sent: ICMP and UDP

You will also notice that multiple paths are included on the map, this is because there are multiple different paths a packet can take to a same destination domain. 


## System Requirements
- python 3.7.0
- pip


## Installation

```
pip install -r requirements.txt
```

## Run

```
python main.py protocol_type domain_name
```

Example

```
python main.py icmp 8.8.8.8
```

or 

```
python main.py icmp google.com
```

### Example Output
![traceroute output](images/traceroute_map_example.png)
