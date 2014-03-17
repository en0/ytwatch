ytwatch
=======
An Automatic Youtube Downloader.

Dependencys
-----------
pytube
scapy
python2 - Due to dependencies of pytube and scapy, python2 is required.
root access - Scapy creates a promiscuous socket. Running ytdl alone does NOT require elevated privileges.

FILES 
-----
ytdl.py
##
Creates a simple download method using pytube. Run ./ytdl --help for more details
  
ytwatch.py
##
Monitors network traffic using scapy and caputures all GET requests to youtube.com/watch?v=. The resource is extracted and the ytdl tool is called to download the resource.
