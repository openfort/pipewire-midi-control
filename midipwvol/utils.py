import subprocess
import json
import re
import os

NODE_FILE = 'node_names.json'

### Helper Functions
## read, write json for permanent config
# Load existing data
def load_nodes():
    if os.path.exists(NODE_FILE):
        with open(NODE_FILE, 'r') as f:
            return json.load(f)
    return {}

# Save data to file
def save_nodes(data):
    with open(NODE_FILE, 'w') as f:
        json.dump(data, f, indent=2)

# Add or update a node by channel number
def add_node(channel, node_name):
    data = load_nodes()
    data[str(channel)] = node_name
    save_nodes(data)

# Get a node by channel number
def get_node(channel):
    data = load_nodes()
    return data.get(str(channel))

# Remove a node by channel
def remove_node(channel):
    data = load_nodes()
    if str(channel) in data:
        del data[str(channel)]
        save_nodes(data)

def get_child_pid(parent):
    result = subprocess.run(['pstree', '-p', '-T', '-A', str(parent)],
                        capture_output=True, text=True).stdout

    #print(result)
    result = re.sub(r'^[^-]*', '', result)
    lines = result.strip().split('\n')

    first_layer_pids = [parent]
    for line in lines:
        line = line.replace(' ', '')  # Remove all whitespace
        if line.startswith('-+-') or line.startswith('|-') or line.startswith('`-'):
            match = re.search(r'\((\d+)\)', line)
            if match:
                first_layer_pids.append(match.group(1))
    return first_layer_pids

def get_node_name():
    result = (subprocess.run(['qdbus', 'org.kde.KWin', '/KWin', 'org.kde.KWin.queryWindowInfo'], capture_output=True, text=True)).stdout.strip()
    # Parse the output to find pid
    for line in result.split('\n'):
        if 'pid' in line:
            pid = line.split(' ')[1]
            #print(pid)
            result = subprocess.run(['pw-dump'], capture_output=True, text=True)
            objects = json.loads(result.stdout)

            for pid in get_child_pid(pid):
                #print(pid)
                for obj in objects:
                    props = obj.get('info', {}).get('props', {})
                    obj_pid = props.get('application.process.id')
                    if obj_pid is not None:
                        if int(obj_pid) == int(pid):
                            node_name = obj['info']['props'].get('node.name')
                            if node_name is not None:
                                return node_name
    return None
