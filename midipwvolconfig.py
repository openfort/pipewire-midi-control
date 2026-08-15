# Custom user configuration.
# Should be located at ~/.config/midipwvol/midipwvolconfig.py


from midipwvol.utils import interp
import subprocess
import json
import dbus
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

### Actual Config
def handle_midi_message(port, message, pw, ddc):
    ## Audio Devices
    if message.is_cc(8):
        pw(type="Node", node_description="HyperX 7.1 Audio Analog Stereo", is_audio=True, is_source=True).set_volume(message.value / 127)
    elif message.is_cc(9):
        pw(type="Node", node_description="HyperX 7.1 Audio Analog Stereo", is_audio=True, is_sink=True).set_volume(message.value / 127)
        pw(type="Node", node_description="GA102 High Definition Audio Controller Digital Stereo (HDMI)", is_audio=True, is_sink=True).set_volume(message.value / 127)

    ## Programs
    # Spotify
    elif message.is_cc(1):
        subprocess.run(['playerctl', '--player=spotify', 'volume', f'{(message.value/127):.2}'])
        #pw(type="Node", node_name="spotify", is_audio=True, is_source=True).set_volume(message.value / 127)
    elif message.type == 'note_on' and message.note == 8:
        pw(type="Node", node_name="spotify", is_audio=True, is_source=True).set_volume(volume=None,mute=True)
    elif message.type == 'note_off' and message.note == 8:
        pw(type="Node", node_name="spotify", is_audio=True, is_source=True).set_volume(volume=None,mute=False)

    # others dynamically
    elif message.type == 'note_on' and message.note < 8 and message.note > 1:
        node_name = get_node_name()
        if node_name is not None:
            add_node(message.note+1, node_name)
            print(node_name)
        else:
            remove_node(message.note+1)
    elif message.type == 'control_change':
        node_name = get_node(message.control)
        if node_name is not None:
            pw(type="Node", node_name=node_name, is_audio=True, is_source=True).set_volume(message.value / 127)
    elif message.type == 'note_on' and message.note >= 9 and message.note <= 15:
        node_name = get_node(message.note-7)
        pw(type="Node", node_name=node_name, is_audio=True, is_source=True).set_volume(volume=None,mute=True)
    elif message.type == 'note_off' and message.note >= 9 and message.note <= 15:
        node_name = get_node(message.note-7)
        pw(type="Node", node_name=node_name, is_audio=True, is_source=True).set_volume(volume=None,mute=False)

    ## Media Keys
    elif message.type == 'note_on' and message.note == 22:
        subprocess.run(['playerctl', '--player=spotify', 'play-pause'])
    elif message.type == 'note_on' and message.note == 18:
        subprocess.run(['playerctl', '--player=spotify', 'previous'])
    elif message.type == 'note_on' and message.note == 19:
        subprocess.run(['playerctl', '--player=spotify', 'next'])

    ## Display
    elif message.type == 'note_on' and message.note == 16:
        # Display brightness change:
        brightness = ddc.get_brightness(display_num=2)
        #print(brightness)
        if ddc.get_brightness(display_num=2) > 50:
            ddc.set_brightness(0, display_num=2)
        else:
            ddc.set_brightness(60, display_num=2)
