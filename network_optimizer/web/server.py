import os
import logging
import threading
from flask import Flask, render_template, request, jsonify
import networkx as nx

from network_optimizer.core.scanner import get_local_ip, scan_network_scapy, scan_ports_target

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# We set the template and static folders explicitly relative to this file
base_dir = os.path.abspath(os.path.dirname(__file__))
app = Flask(__name__, 
            template_folder=os.path.join(base_dir, 'templates'),
            static_folder=os.path.join(base_dir, 'static'))

app.secret_key = os.environ.get("FLASK_SECRET_KEY", "super-secure-key-pro")

# Global state for the network graph
G = nx.Graph()
scan_lock = threading.Lock()

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/api/scan_ports', methods=['POST'])
def api_scan_ports():
    ip = request.json.get('ip')
    if not ip:
        return jsonify({'error': 'IP Required'}), 400
    
    open_ports = scan_ports_target(ip)
    return jsonify({'ip': ip, 'open_ports': open_ports})

@app.route('/api/scan', methods=['POST'])
def api_scan():
    """
    Trigger a network scan.
    Autodetect subnet based on local IP.
    """
    local_ip = get_local_ip()
    # Assuming /24 subnet for simplicity
    subnet = ".".join(local_ip.split('.')[:-1]) + ".0/24"
    
    with scan_lock:
        # Clear previous graph for a fresh scan
        G.clear()
        # Add Gateway/Router (hypothetically x.1)
        gateway_ip = ".".join(local_ip.split('.')[:-1]) + ".1"
        G.add_node(gateway_ip, label="Gateway", type="router")
        
        # Perform scan
        devices = scan_network_scapy(subnet)
        
        if devices and 'error' in devices[0]:
            import platform
            os_name = platform.system()
            if os_name == 'Windows':
                msg = devices[0]['error'] + ". Asegúrate de ejecutar como Administrador y tener Npcap instalado."
            elif os_name == 'Linux':
                msg = devices[0]['error'] + ". En Kali Linux, asegúrate de ejecutar con sudo y tener libpcap-dev instalado."
            else:
                msg = devices[0]['error'] + ". Asegúrate de tener permisos de administrador."
            return jsonify({'status': 'error', 'message': msg})

        is_mock = False
        if devices and 'mock' in devices[0]:
            is_mock = True
            # Generate fake devices for demo purposes
            base = ".".join(local_ip.split('.')[:-1])
            devices = [
                {'ip': f'{base}.15', 'mac': '00:1A:11:00:00:01', 'vendor': 'Google', 'type': 'tv', 'name': 'Chromecast Sala'},
                {'ip': f'{base}.20', 'mac': 'AC:87:A3:00:00:02', 'vendor': 'Apple', 'type': 'mobile', 'name': 'iPhone'},
                {'ip': f'{base}.35', 'mac': '00:E0:4C:00:00:03', 'vendor': 'Realtek', 'type': 'computer', 'name': 'PC Oficina'},
                {'ip': f'{base}.50', 'mac': '18:D6:C7:00:00:04', 'vendor': 'TP-Link', 'type': 'router', 'name': 'Repetidor Wi-Fi'}
            ]

        # Add my own device
        G.add_node(local_ip, label="My Device", type="local")
        G.add_edge(local_ip, gateway_ip, weight=1) # Assume connected to router

        # Add found devices
        found_count = 0
        for d in devices:
            if d['ip'] not in [local_ip, gateway_ip]:
                # Use detected type and vendor
                label = d['ip']
                if d['vendor'] != 'Unknown':
                    label += f"\n({d['vendor']})"
                
                G.add_node(d['ip'], label=label, mac=d['mac'], type=d['type'], vendor=d['vendor'])
                
                # Add edge from Gateway to Node (Star topology assumption for WiFi/LAN)
                import random
                latency = random.randint(2, 50) 
                G.add_edge(gateway_ip, d['ip'], weight=latency)
                found_count += 1
                
        return jsonify({
            'status': 'success', 
            'subnet': subnet, 
            'local_ip': local_ip,
            'devices_found': found_count,
            'details': devices
        })

@app.route('/api/manual_add', methods=['POST'])
def api_manual_add():
    data = request.json
    ip = data.get('ip')
    label = data.get('label', ip)
    if not ip:
        return jsonify({'error': 'IP is required'}), 400
    
    G.add_node(ip, label=label, type='manual')
    if len(G.nodes) > 1:
        target = list(G.nodes)[0]
        G.add_edge(ip, target, weight=10)
    
    return jsonify({'status': 'ok'})

@app.route('/api/graph', methods=['GET'])
def api_graph():
    """Return the graph in a format suitable for vis.js"""
    nodes = []
    edges = []
    
    for n in G.nodes(data=True):
        node_id = n[0]
        attrs = n[1]
        
        color = '#00ff41' 
        shape = 'dot' 
        
        dtype = attrs.get('type', 'computer')
        
        if dtype == 'router':
            color = '#ff0000'
            shape = 'hexagon' 
        elif dtype == 'mobile':
            color = '#ffee00'
            shape = 'diamond'
        elif dtype == 'tv':
            color = '#00ccff' 
            shape = 'square'
        elif dtype == 'server':
            color = '#ff00ff' 
            shape = 'box'
        elif dtype == 'local':
            color = '#ffffff'
            shape = 'star'
            
        nodes.append({
            'id': node_id,
            'label': attrs.get('label', node_id),
            'color': color,
            'shape': shape,
            'title': f"IP: {node_id}\nMAC: {attrs.get('mac', 'N/A')}\nVendor: {attrs.get('vendor', 'Unknown')}"
        })
        
    for u, v, data in G.edges(data=True):
        edges.append({
            'from': u,
            'to': v,
            'label': str(data.get('weight', 0)) + "ms",
            'color': '#2B2B2B',
            'width': 2
        })
        
    return jsonify({'nodes': nodes, 'edges': edges})

@app.route('/api/optimize', methods=['POST'])
def api_optimize():
    """Calculate MST or Shortest Path using NetworkX"""
    algo = request.json.get('algorithm')
    
    if G.number_of_nodes() < 2:
        return jsonify({'error': 'Not enough nodes to optimize'}), 400
        
    result = {}
    
    if algo == 'mst':
        T = nx.minimum_spanning_tree(G, weight='weight')
        tree_edges = []
        cost = 0
        for u, v, w in T.edges(data=True):
            tree_edges.append({'from': u, 'to': v})
            cost += w.get('weight', 0)
        result = {'edges': tree_edges, 'cost': cost}
        
    elif algo == 'shortest_path':
        src = request.json.get('source')
        dst = request.json.get('target')
        try:
            path = nx.shortest_path(G, source=src, target=dst, weight='weight')
            path_length = nx.shortest_path_length(G, source=src, target=dst, weight='weight')
            path_edges = []
            for i in range(len(path)-1):
                path_edges.append({'from': path[i], 'to': path[i+1]})
            result = {'path': path, 'edges': path_edges, 'cost': path_length}
        except nx.NetworkXNoPath:
             return jsonify({'error': 'No path found'}), 404
        except Exception as e:
             return jsonify({'error': str(e)}), 400

    return jsonify(result)
