import socket
import server
import client

#key: ip
#value: [name, money]
players = dict()

def get_ip():
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    try:
        # doesn't even have to be reachable
        s.connect(('10.255.255.255', 1))
        IP = s.getsockname()[0]
    except:
        IP = 'localhost'
    finally:
        s.close()
    return IP

