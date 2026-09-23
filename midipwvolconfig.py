# Custom user configuration.
# Should be located at ~/.config/midipwvol/midipwvolconfig.py

from midipwvol.utils import load_nodes, save_nodes, add_node, get_node, remove_node, get_child_pid, get_node_name, start_app, send_msg
import subprocess
import json

### Actual Config
def handle_midi_message(port, message, pw, ddc):
    device_name = "X-TOUCH MINI"
    if port.name.find(device_name) == -1:
        return
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
        if start_app('spotify') == True:
            pw(type="Node", node_name="spotify", is_audio=True, is_source=True).set_volume(volume=None,mute=True)
    elif message.type == 'note_off' and message.note == 8:
        if start_app('spotify') == True:
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
        if start_app(node_name) == True:
            pw(type="Node", node_name=node_name, is_audio=True, is_source=True).set_volume(volume=None,mute=True)
    elif message.type == 'note_off' and message.note >= 9 and message.note <= 15:
        node_name = get_node(message.note-7)
        if start_app(node_name) == True:
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
