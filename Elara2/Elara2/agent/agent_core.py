# agent_core.py - Main agent for Elara system
import socket, time, os, platform, uuid, json
from datetime import datetime

CONFIG = 'agent/config/device_map.json'
MACS = 'agent/config/mac_whitelist.json'
LOG = 'logs/device_status_log.csv'

def get_mac(): return ':'.join(['{:02x}'.format((uuid.getnode() >> i) & 0xff) for i in range(0,8*6,8)][::-1]).upper()
def check_mac(): return get_mac() in [m.upper() for m in json.load(open(MACS))]

def ping(ip): return os.system(f"ping -{'n' if platform.system()=='Windows' else 'c'} 1 {ip} > nul 2>&1") == 0
def check_port(ip, port): 
    try: socket.create_connection((ip, port), timeout=2).close(); return True
    except: return False

def log(msg):
    now = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    print(f"[{now}] {msg}")
    with open(LOG, 'a') as f: f.write(f"{now},{msg}\n")

def run():
    if not check_mac(): return log("❌ Unauthorized MAC.")
    devices = json.load(open(CONFIG))
    while True:
        for d in devices:
            name, ip, port = d['name'], d['ip'], d['port']
            log(f"{name} ({ip}:{port}) - Ping: {'OK' if ping(ip) else 'FAIL'} | Port: {'Open' if check_port(ip, port) else 'Closed'}")
        time.sleep(10)

if __name__ == '__main__': run()
