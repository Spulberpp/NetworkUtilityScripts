#!/usr/bin/python3
import socket
import struct
import sys
import subprocess
import threading

d, s, c = socket.inet_aton, struct, '!I'
f = lambda n: s.pack(c, n)
g = lambda n: socket.inet_ntoa(f(n))

def h(n, b):
    t = 32 - int(b)
    u = s.unpack(c, d(n))[0]
    v = (u >> t) << t
    w = v | ((1 << t) - 1)
    return g(v), g(w), [g(x) for x in range(v, w + 1)]

def ping(ip):
    try:
        output = subprocess.check_output(['ping', '-c', '1', '-W', '1', ip])
        if "1 received" in output.decode('utf-8'):
            return True
        else:
            return False
    except subprocess.CalledProcessError:
        return False

def scan_ports(ip, ports):
    open_ports = []
    for port in ports:
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.settimeout(1)
        result = sock.connect_ex((ip, port))
        if result == 0:
            open_ports.append(port)
        sock.close()
    return open_ports

if len(sys.argv) < 2:
    print("Usage: python subnet_to_iprange.py <subnet>")
    print("Example: python subnet_to_iprange.py 192.168.1.0/24")
    sys.exit(1)

subnet = sys.argv[1]
start, end, ips = h(*subnet.split('/'))

print(f'Subnet: {subnet}')
print(f'IP Range: {start} - {end}')
print('All IPs:')

# Define the ports you want to scan
ports_to_scan = range(1, 1025)

for i in ips:
    status = "up" if ping(i) else "down"
    color = "\033[32m" if status == "up" else "\033[31m"
    open_ports = scan_ports(i, ports_to_scan)
    print(f'{color}{i}  \033[0m (Status: {status}, Open Ports: {open_ports})')
