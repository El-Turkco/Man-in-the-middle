import subprocess as sub

def ip_forwarding():
    sub.call(["echo","1",">","/proc/sys/net/ipv4/ip_forward"])


