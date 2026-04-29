import socket
import logging
from typing import List, Dict, Any

logger = logging.getLogger(__name__)

def get_local_ip():
    """Detects the local IP address."""
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    try:
        # dest doesn't need to be reachable
        s.connect(('10.255.255.255', 1))
        IP = s.getsockname()[0]
    except Exception:
        IP = '127.0.0.1'
    finally:
        s.close()
    return IP

def get_mac_vendor(mac):
    """
    Simple MAC OUI lookup. In a real app, use an API or local DB.
    Here we use a small heuristic map for demo/speed.
    """
    mac_prefix = mac.upper().replace(':', '')[:6]
    vendors = {
        'B827EB': 'Raspberry Pi', 'DCA632': 'Raspberry Pi',
        '00E04C': 'Realtek', '546009': 'Google', # Google Home/Chromecast
        '001A11': 'Google',
        'AC87A3': 'Apple', 'A45E60': 'Apple', '3C15C2': 'Apple', # iPhones/Macs
        'BC6EE2': 'Samsung', '24F5AA': 'Samsung',
        '18D6C7': 'TP-Link', '60E327': 'TP-Link',
        'C025E9': 'TP-Link',
        'E894F6': 'Xiaomi', '640980': 'Xiaomi',
        '00265B': 'Hitron', '00145C': 'Cisco',
        'D850E6': 'Asus', 'F07959': 'Asus',
        '4CE676': 'Buffalo',
        'DCFB48': 'Netgear',
        'EC8A89': 'Starlink'
    }
    # Try 6 char prefix
    if mac_prefix in vendors: return vendors[mac_prefix]
    # Try known "generic" brands from full string lookups or other APIs?
    # For now return Unknown
    return "Unknown"

def guess_device_type(mac, vendor):
    """Guess device type icon based on Vendor."""
    vendor = vendor.lower()
    if 'apple' in vendor or 'samsung' in vendor or 'xiaomi' in vendor:
        return 'mobile'
    if 'raspberry' in vendor:
        return 'server'
    if 'google' in vendor:
        return 'tv' # Chromecast/Home
    if 'tp-link' in vendor or 'netgear' in vendor or 'asus' in vendor or 'cisco' in vendor or 'hitron' in vendor:
        return 'router'
    return 'computer'

def scan_network_scapy(ip_range: str) -> List[Dict[str, Any]]:
    """
    Real network scan using Scapy ARP requests.
    Attempts to identify device type and vendor.
    """
    devices = []
    try:
        from scapy.all import ARP, Ether, srp
        logger.info(f"Scanning network: {ip_range}")
        
        # Create ARP request
        arp = ARP(pdst=ip_range)
        ether = Ether(dst="ff:ff:ff:ff:ff:ff")
        packet = ether/arp

        # Send packet and capture response
        # Increased timeout slightly for better detection
        result = srp(packet, timeout=3, verbose=0)[0]

        for sent, received in result:
            mac = received.hwsrc
            vendor = get_mac_vendor(mac)
            dtype = guess_device_type(mac, vendor)
            
            devices.append({
                'ip': received.psrc,
                'mac': mac,
                'vendor': vendor,
                'type': dtype,
                'name': vendor if vendor != "Unknown" else received.psrc
            })
            
    except ImportError:
        logger.error("Scapy missing")
        return [{'error': 'Scapy library missing'}]
    except Exception as e:
        logger.error(f"Scan error: {e}")
        if "Operation not permitted" in str(e) or "not permitted" in str(e).lower():
            return [{'mock': True}]
        return [{'error': str(e)}]
        
    return devices

def basic_ping_scan(subnet_base: str):
    """
    Fallback scan using basic socket connection attempts (pseudo-ping).
    Faster and doesn't require admin rights (usually), but less accurate for non-server devices.
    """
    devices = []
    # Scan only first 20 and last 20 for speed in demo, or full 254 in async
    # For this "Pro" app, let's just do a limited range to keep UI responsive 
    # or rely on the user to wait.
    pass

def scan_ports_target(ip: str):
    """
    Scans common ports on the target IP.
    """
    common_ports = [21, 22, 23, 25, 53, 80, 110, 135, 139, 143, 443, 445, 993, 995, 3306, 3389, 5900, 8080]
    open_ports = []
    
    for port in common_ports:
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.settimeout(0.5)
        try:
            result = s.connect_ex((ip, port))
            if result == 0:
                # Try to grab banner
                banner = ""
                try:
                    s.send(b'HEAD / HTTP/1.0\r\n\r\n')
                    banner = s.recv(1024).decode('utf-8', errors='ignore').strip().split('\n')[0]
                except:
                    pass
                open_ports.append({'port': port, 'banner': banner[:50]})
        except Exception:
            pass
        finally:
            s.close()
    return open_ports
