#!/usr/bin/env python3
from datetime import datetime
import subprocess
from collections import defaultdict
import yaml
# import time
# import signal
# import sys
import json
import os
# import threading
from threading import Lock
from threading import Thread

# External modules
from scapy.all import sniff, DNS, IP, UDP, ARP, Ether, srp
# from scapy.all import conf
from colorama import Fore
from flask import Flask, render_template_string, Response
# debug stuff ----------------------------
from scapy.config import conf
conf.debug_dissector = 2


# Dictionary to store host information, keyed by MAC address
host_data = defaultdict(lambda: {
    'ip': None,  # Store the IP address
    'count': 0,
    'last_seen': None,
    'hostname': None,
    'method': None,
    "vendor": None,
    'services': set()  # Store unique services as a set
})

# Path to the YAML file
YAML_FILE = 'devices.yml'
data_lock = Lock()
run = True
ip_to_mac = {}
DEBUG = True
LAN = "10.0.1."
# Threading event to signal shutdown
# gRun = threading.Event()

def arp_ping(net):
    ans, unans = srp(Ether(dst="ff:ff:ff:ff:ff:ff")/ARP(pdst=net), timeout=2)
    for r in ans.res:
        mac = r.answer[ARP].hwsrc
        ip = r.answer[ARP].psrc
        name, method = get_hostname(ip)
        vendor = conf.manufdb.lookup(mac)[1]
        host_data[mac]
        host_data[mac]["ip"] = ip
        host_data[mac]["method"] = "arp"
        host_data[mac]["vendor"] = vendor
        if name:
            host_data[mac]["hostname"] = name
        ip_to_mac[ip] = mac
        debug(f"ARPING: {mac}|{ip} -> {name}[{vendor}]", Fore.GREEN)

def debug(string, color):
    if not DEBUG: return
    print(f"{color}{string}{Fore.RESET}", flush=True)

def get_hostname(ip):
    """Attempt to resolve IP to hostname using nslookup with DNS server 10.0.1.200."""
    try:
        result = subprocess.run(
            ['nslookup', ip, '10.0.1.200'],
            capture_output=True,
            text=True,
            timeout=5
        )
        output = result.stdout
        for line in output.splitlines():
            if 'name =' in line.lower():
                hostname = line.split('name =')[-1].strip().rstrip('.')
                return hostname, "socket"
        return None, None
    except (subprocess.SubprocessError, UnicodeDecodeError):
        return None, None

def handle_dns_pkt(packet):
    """
    FIXME: this never prints debug messages
    """
    if packet[DNS].qr != 1:  # DNS response
        debug(f"ERROR: invalid DNS from {packet[DNS].an[i].rdata}")
        return

    for i in range(packet[DNS].ancount):
        if hasattr(packet[DNS].an[i], 'rdata'):
            if isinstance(packet[DNS].an[i].rdata, str):
                ip = packet[DNS].an[i].rdata
                # Only update if IP is in 10.0.1.0/24 and has a known MAC
                if ip.startswith(LAN) and ip in ip_to_mac:
                    mac = ip_to_mac[ip]
                    hostname = packet[DNS].an[i].rrname.decode('utf-8').rstrip('.')
                    host_data[mac]['hostname'] = hostname
                    host_data[mac]['method'] = "DNS"
                    debug(f"DNS rdata: {mac}|{ip} -> {host_data[mac]["hostname"]}", Fore.YELLOW)

def handle_mdns_pkt(packet):
    if packet[DNS].qr != 1:  # mDNS response
        return

    for i in range(packet[DNS].ancount):
        if hasattr(packet[DNS].an[i], 'rdata'):
            if isinstance(packet[DNS].an[i].rdata, str):
                ip = packet[DNS].an[i].rdata
                # Only update if IP is in 10.0.1.0/24 and has a known MAC
                if ip.startswith(LAN) and ip in ip_to_mac:
                    mac = ip_to_mac[ip]
                    hostname = packet[DNS].an[i].rrname.decode('utf-8').rstrip('.')
                    host_data[mac]['hostname'] = hostname
                    host_data[mac]['method'] = "mDNS"
                    debug(f"mDNS rdata: {mac}|{ip} -> {host_data[mac]["hostname"]}", Fore.MAGENTA)
        # Extract mDNS service information (PTR records for services)
        if packet[DNS].an[i].type == 12:  # PTR record
            service = packet[DNS].an[i].rrname.decode('utf-8').rstrip('.')
            if service.endswith(('_tcp.local', '_udp.local')):
                ip = packet[IP].src
                # Only update if source IP is in 10.0.1.0/24 and has a known MAC
                if ip.startswith(LAN) and ip in ip_to_mac:
                    mac = ip_to_mac[ip]
                    host_data[mac]['services'].add(service)
                    debug(f"mDNS PTR: {mac}|{ip} -> {host_data[mac]["hostname"]}", Fore.MAGENTA)

def packet_callback(packet):
    global host_data
    global ip_to_mac

    if ARP in packet and packet[ARP].op in (1,2): #who-has or is-at
        mac_src = packet[ARP].hwsrc
        ip_src = packet[ARP].psrc

        ip_to_mac[ip_src] = mac_src
        
        if mac_src not in host_data:
            host_data[mac_src]

        host_data[mac_src]['ip'] = ip_src
        host_data[mac_src]['count'] += 1
        host_data[mac_src]['method'] = "arp"
        vendor = conf.manufdb.lookup(mac_src)[1]
        host_data[mac_src]["vendor"] = vendor

        if not host_data[mac_src]['hostname']:
            hostname, method = get_hostname(ip_src)
            if hostname:
                host_data[mac_src]['hostname'] = hostname

        debug(f"ARP: {mac_src}|{ip_src} -> {host_data[mac_src]["hostname"]}", Fore.CYAN)


    """Process each captured packet."""
    # if IP in packet and Ether in packet:
    if IP not in packet or Ether not in packet: return

    ip_src = packet[IP].src
    mac_src = packet[Ether].src
    # print(ip_src,mac_src)
    # print('.', end='',flush=True)
    
    # Only process source IPs in the 10.0.1.0/24 subnet
    if not ip_src.startswith('10.0.1.'):
        debug(f"ERROR: Invalid IP: {ip_src}", Fore.RED)
        return

    # Update IP-to-MAC mapping
    ip_to_mac[ip_src] = mac_src
    
    if mac_src not in host_data:
        host_data[mac_src]

    # Update host data for MAC address
    host_data[mac_src]['ip'] = ip_src
    host_data[mac_src]['count'] += 1
    host_data[mac_src]['last_seen'] = datetime.now()
    vendor = conf.manufdb.lookup(mac_src)[1]
    host_data[mac_src]["vendor"] = vendor

    if not host_data[mac_src]['hostname']:
        hostname, method = get_hostname(ip_src)
        if hostname:
            host_data[mac_src]['hostname'] = hostname
            host_data[mac_src]['method'] = method or "Unknown"

    # Handle DNS and mDNS packets
    # if packet.haslayer(DNS) and packet.haslayer(UDP):
    if not packet.haslayer(DNS) or not packet.haslayer(UDP): return

    # Check for standard DNS (port 53) or mDNS (port 5353)
    if packet[UDP].sport == 53 or packet[UDP].dport == 53:
        handle_dns_packet(packet)

    elif packet[UDP].sport == 5353 or packet[UDP].dport == 5353:
        handle_mdns_pkt(packet)

def save_to_yaml():
    """Write host_data to devices.yml every SAVE_INTERVAL seconds."""
    try:
        # Convert host_data to YAML-compatible format
        yaml_data = {}
        for mac, data in host_data.items():
            yaml_data[mac] = {
                'ip': data['ip'],
                'hostname': data['hostname'],
                'method': data['method'],
                "vendor": data["vender"],
                'services': list(data['services'])  # Convert set to list for YAML
            }
        # Write to devices.yml
        with open('devices.yml', 'w') as f:
            yaml.dump(yaml_data, f, default_flow_style=False)
            
    except Exception as e:
        print(f"Error writing to YAML: {e}")

def print_summary():
    """Print summary of captured data, including services."""
    print("\n=== Network Capture Summary ===")
    print(f"{'MAC Address':<18} {'IP Address':<11} {'Hostname':<20} {'Last Seen':<20} {'Services'}")
    print("-" * 130)
    for mac, data in sorted(host_data.items(), key=lambda x: int(x[1]['ip'].split(".")[3]), reverse=False):
        # print(f">> data['last_seen']: {type(data['last_seen'])}")
        ip = data['ip'] or "Unknown"
        hostname = (data['hostname'][:26] + '...') if data['hostname'] and len(data['hostname']) > 29 else data['hostname'] or "Unknown"
        last_seen = data['last_seen'].strftime('%Y-%m-%d %H:%M:%S') if data['last_seen'] else "Never"
        method = data['method'] if data['method'] else "Unknown"
        services = ', '.join(data['services'])[:29] if data['services'] else "None"
        print(f"{mac:<18} {ip:<11} {hostname:<20} {last_seen:<20} {services}")
    print("\n")

def listen_main():
    global run

    arp_ping(LAN + "0/24")

    try:
        while run:
            # # print(".",end='',flush=True)
            sniff_filter = "udp port 53 or udp port 5353 or ip or arp"
            # sniff_filter = "src net 10.0.1.0/24 and (udp port 53 or udp port 5353 or ip or arp)"
            sniff(prn=packet_callback, filter=sniff_filter, timeout=1.0, iface="en0", store=False)
    # except Exception as e:
    #     print(f"{Fore.RED}e{Fore.RESET}")
    finally:
        print(f"{Fore.GREEN}/// listen_main() finished ///{Fore.RESET}")
        save_to_yaml()
        print(f"{Fore.GREEN}/// Saving host_data to {YAML_FILE} ///{Fore.RESET}")
    # Set up Ctrl+C handler
    # signal.signal(signal.SIGINT, signal_handler)
    
    # try:
        # print(f"Starting network capture (including mDNS) for 10.0.1.0/24, saving to devices.yml every {SAVE_INTERVAL} seconds... Press Ctrl+C to stop")
        # Start the YAML-saving thread
        # yaml_thread = threading.Thread(target=save_to_yaml, daemon=True)
        # yaml_thread.start()
        
        # Start packet sniffing
    # except KeyboardInterrupt:
    #     print("\nCapture stopped by user.")
    # except Exception as e:
    #     print(f"Error occurred: {e}")
    # finally:
    #     # shutdown_event.set()  # Ensure the YAML thread stops
    #     # Save final state to YAML
    #     try:
    #         yaml_data = {}
    #         for mac, data in host_data.items():
    #             yaml_data[mac] = {
    #                 'ip': data['ip'],
    #                 'count': data['count'],
    #                 'last_seen': data['last_seen'].strftime('%Y-%m-%d %H:%M:%S') if data['last_seen'] else None,
    #                 'hostname': data['hostname'],
    #                 'method': data['method'],
    #                 'services': list(data['services'])
    #             }
    #         with open('devices.yml', 'w') as f:
    #             yaml.dump(yaml_data, f, default_flow_style=False)
    #     except Exception as e:
    #         print(f"Error writing final YAML: {e}")
        # print_summary()


app = Flask(__name__)

# HTML template with dark mode theme and sorting
HTML_TEMPLATE = '''
<!DOCTYPE html>
<html>
<head>
    <title>Device Information</title>
    <style>
        body {
            background-color: #1e1e1e;
            color: #d4d4d4;
            font-family: Arial, sans-serif;
        }
        h2 {
            color: #ffffff;
        }
        table {
            border-collapse: collapse;
            width: 100%;
            margin-top: 20px;
            background-color: #2d2d2d;
        }
        th, td {
            border: 1px solid #444;
            padding: 8px;
            text-align: left;
        }
        th {
            background-color: #3c3c3c;
            color: #ffffff;
            cursor: pointer;
        }
        th:hover {
            background-color: #4a4a4a;
        }
        td {
            color: #d4d4d4;
        }
        tr:nth-child(even) {
            background-color: #333333;
        }
        tr:hover {
            background-color: #3a3a3a;
        }
        .sort-asc::after { content: ' ▲'; color: #bb86fc; }
        .sort-desc::after { content: ' ▼'; color: #bb86fc; }
    </style>
</head>
<body>
    <h2>Device Information</h2>
    <table id="deviceTable">
        <thead>
            <tr>
                <th onclick="sortTable(0, 'string')">Hostname</th>
                <th onclick="sortTable(1, 'ip')">IP</th>
                <th>Hardware Address</th>
                <th>Last Seen</th>
                <th>Count</th>
                <th>Vendor</th>
                <th>Services</th>
            </tr>
        </thead>
        <tbody>
            {% for hw_addr, device in devices.items() %}
            <tr>
                <td>{{ device.hostname }}</td>
                <td>{{ device.ip }}</td>
                <td>{{ hw_addr }}</td>
                <td>{{ device.last_seen }}</td>
                <td>{{ device.count }}</td>
                <td>{{ device.vendor }}</td>
                <td>
                {% for svc in device.services %}
                    <ul>
                        <li>{{ svc }}</li>
                    </ul>
                {% endfor %}
                </td>
            </tr>
            {% endfor %}
        </tbody>
    </table>

    <script>
        let lastSortedColumn = -1;
        let sortDirection = 1;

        function sortTable(col, type) {
            const table = document.getElementById("deviceTable");
            const tbody = table.getElementsByTagName("tbody")[0];
            const rows = Array.from(tbody.getElementsByTagName("tr"));

            // Toggle sort direction if same column is clicked
            if (lastSortedColumn === col) {
                sortDirection *= -1;
            } else {
                sortDirection = 1;
            }
            lastSortedColumn = col;

            // Remove sort indicators
            const headers = table.getElementsByTagName("th");
            for (let header of headers) {
                header.classList.remove("sort-asc", "sort-desc");
            }
            // Add sort indicator
            headers[col].classList.add(sortDirection === 1 ? "sort-asc" : "sort-desc");

            rows.sort((a, b) => {
                let aValue = a.cells[col].textContent.trim();
                let bValue = b.cells[col].textContent.trim();

                if (type === 'ip') {
                    // Convert IP to numerical value for sorting
                    aValue = ipToNumber(aValue);
                    bValue = ipToNumber(bValue);
                    return (aValue - bValue) * sortDirection;
                } else {
                    // String comparison for hostname
                    return aValue.localeCompare(bValue) * sortDirection;
                }
            });

            // Rebuild table body
            while (tbody.firstChild) {
                tbody.removeChild(tbody.firstChild);
            }
            rows.forEach(row => tbody.appendChild(row));
        }

        function ipToNumber(ip) {
            return ip.split('.').reduce((acc, octet) => (acc << 8) + parseInt(octet), 0);
        }
    </script>
</body>
</html>
'''

# Custom JSON encoder to handle datetime objects
class DateTimeEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, datetime):
            return obj.isoformat()
        if isinstance(obj, set):
            return list(obj)
        return super().default(obj)

@app.route('/')
def display_devices():
    with data_lock:
        return render_template_string(HTML_TEMPLATE, devices=host_data)

# @app.route('/yaml')
# def get_yaml():
#     with data_lock:
#         yaml_data = yaml.dump(data, sort_keys=False)
#         return Response(yaml_data, mimetype='application/yaml')

@app.route('/json')
def get_json():
    with data_lock:
        json_data = json.dumps(host_data, indent=2, cls=DateTimeEncoder)
        return Response(json_data, mimetype='application/json')

def load_yaml(filename):
    if os.path.exists(YAML_FILE):
        with open(YAML_FILE, 'r') as file:
            data = yaml.safe_load(file) or {}

        for k,v in data.items():
            host_data[k]
            host_data[k]["ip"] = v["ip"]
            host_data[k]["hostname"] = v["hostname"]
            host_data[k]['method'] = v['method']
            host_data[k]["services"] = set(v["services"])
            ip_to_mac[v["ip"]] = k

def main():
    with data_lock:
        load_yaml(YAML_FILE)

    # listen_t = Thread(target=listen_main, daemon=True)
    listen_t = Thread(target=listen_main, daemon=False)
    listen_t.start()
    
    try:
        app.run(host='0.0.0.0', port=15000, debug=False)
    # except KeyboardInterrupt:
    #     print(f"{Fore.CYAN}ctrl-c ...{Fore.RESET}")
    #     # print(host_data)
    except Exception as e:
        print(f"{Fore.RED}e{Fore.RESET}")
    finally:
        run = False
        print("finally")
        listen_t.join(timeout=1.0)
        print_summary()

if __name__ == '__main__':
    main()