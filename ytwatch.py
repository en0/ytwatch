#!/bin/env python2
from scapy.all import *
from socket import gethostbyname_ex
import ytdl

def main(host):
    _,_,ips = gethostbyname_ex(host)
    seen = set()

    def _catch_get(packet):
        if Raw in packet and packet[IP].dst in ips and "GET /watch?v=" in packet[Raw].load:
            url = packet.load.split(' ')[1]
            if not url in seen:
                seen.add(url)
                resource = "".join(["http://",host,url])
                ytdl.download(resource)
        return None

    sniff(filter="tcp and port 80", prn=_catch_get);

if __name__ == '__main__':
    main("www.youtube.com")

