import nmap

def nmap_scan(target):
    nm = nmap.PortScanner()
    nm.scan(target, '1-1024')
    return nm.all_hosts()
