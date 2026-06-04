import socket
import threading
from concurrent.futures import ThreadPoolExecutor
from datetime import datetime
from zoneinfo import ZoneInfo

lock = threading.Lock()
open_port = []

asia_kol = ZoneInfo("Asia/Kolkata")
now_time = datetime.now(asia_kol)

# PORT SCANNER

def port_scan(ip, port):
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.settimeout(1)
    result = s.connect_ex((ip,port))
    s.close()
    if(result == 0):
        return True
    return False

# THREAD WORKER

def worker(ip,port):
    if(port_scan(ip,port)):
        banner = banner_info(ip, port)
        port_detail = get_service(port)
        with lock:
            print(f"[OPEN] PORT{"":<5} {port:<5} -> {port_detail} ")
            open_port.append(port)

# BANNER INFOR (TECH STACK, SERVICE etc...)

def banner_info(ip, port):
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.settimeout(2)
        s.connect((ip,port))
        s.send(b"HEAD / HTTP/1.0\r\n\r\n")
        banner = s.recv(1024).decode().strip()
        return banner if banner else "no banner"
    except:
        return "Service not able to find'"
    
SERVICES = {
            20: "FTP-DATA", 21: "FTP", 22: "SSH", 23: "TELNET", 25: "SMTP",
            53: "DNS", 80: "HTTP", 110: "POP3", 111: "RPC", 135: "MSRPC",
            139: "NETBIOS", 143: "IMAP", 443: "HTTPS", 445: "SMB", 993: "IMAPS",
            995: "POP3S", 1433: "MSSQL", 3306: "MYSQL", 3389: "RDP", 
            5432: "POSTGRESQL", 5900: "VNC", 6379: "REDIS", 8080: "HTTP-ALT",
            8443: "HTTPS-ALT", 27017: "MONGODB"
}

def get_service(port):
    return SERVICES.get(port, "UNKNOWN")
    
# EXPORT REPORT TO 'filename.txt'

def export_report(target, host, open_port, now_time):
    with open("scan_report.txt", 'a') as f:
        f.writelines(f"""
{"-"*24} SCAN REPORT ON {now_time} {"-"*24}    
                
{'HOST':<20} : {host}
{'TARGET IP':<20} : {target}
{'OPEN PORTS':<20} : {sorted(open_port)}
{'TIME':<20} : {now_time}

{"-"*60}

""")
        
# END OF FUNCTIONS
            
start_port = 1
end_port = 65535

target = input("Enter the target ip address : ")
try:
    host = socket.gethostbyaddr(target)[0]
except:
    host = "N/A"

print(f"\nScanning started on target ip address : {target}")
print("-"*60)
print("OPEN/CLOSE       PORT        SERVICE")

with ThreadPoolExecutor(max_workers=200) as executors:
    for port in range(start_port, end_port+1):
        executors.submit(worker, target, port)

# for i in range(start_port, end_port+1):
#     t = threading.Thread(target=worker,args=(target,i))
#     threads.append(t)
#     t.start()

# for t in threads:
#     t.join()

print("-"*60)

print("-"*10,end="")
print("FINAL REPORT",end="")
print("-"*10)

print(f"\n{'TARGET IP':<20} : {target:<10}")
print(f"{'HOST':<20} : {host}")
print(f"{'TIME':<20} : {now_time.strftime("%d/%m/%y  :  %H:%M")}")
print(f"{'PORT':<20} : {sorted(open_port)}")
print(f"{'TOTAL PORTS':<20} : {len(open_port)} PORT(S)")
export_report(target,host,open_port, now_time.strftime('%d-%m-%y at %H:%M:%S'))
print(f"REPORT SAVES AS SCAN_REPORT.txt")
print("-"*60)