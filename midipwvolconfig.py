# Custom user configuration.
# Should be located at ~/.config/midipwvol/midipwvolconfig.py


from midipwvol.utils import interp
import subprocess

def handle_midi_message(port, message, pw, ddc):
    # Programs
    if message.is_cc(0):
        pw(type="Node", node_description="HyperX 7.1 Audio Analog Stereo", is_audio=True, is_sink=True).set_volume(message.value / 127)
    elif message.is_cc(1):
        subprocess.run(['playerctl', '--player=spotify', 'volume', f'{(message.value/127):.2}'])
        #pw(type="Node", node_name="spotify", is_audio=True, is_source=True).set_volume(message.value / 127)
    elif message.is_cc(3):
        pw(type="Node", node_name="Brave", is_audio=True, is_source=True).set_volume(message.value / 127)

    # Audio Devices
    elif message.is_cc(8):
        pw(type="Node", node_description="HyperX 7.1 Audio Analog Stereo", is_audio=True, is_source=True).set_volume(message.value / 127)
    elif message.is_cc(9):
        pw(type="Node", node_description="HyperX 7.1 Audio Analog Stereo", is_audio=True, is_sink=True).set_volume(message.value / 127)
        pw(type="Node", node_description="GA102 High Definition Audio Controller Digital Stereo (HDMI)", is_audio=True, is_sink=True).set_volume(message.value / 127)

    # Media Keys
    elif message.type == 'note_on' and message.note == 22:
        subprocess.run(['playerctl', '--player=spotify', 'play-pause'])
    elif message.type == 'note_on' and message.note == 18:
        subprocess.run(['playerctl', '--player=spotify', 'previous'])
    elif message.type == 'note_on' and message.note == 19:
        subprocess.run(['playerctl', '--player=spotify', 'next'])

    # Display
    elif message.type == 'note_on' and message.note == 16:
        # Display brightness change:
        brightness = ddc.get_brightness(display_num=2)
        #print(brightness)
        if ddc.get_brightness(display_num=2) > 50:
            ddc.set_brightness(0, display_num=2)
        else:
            ddc.set_brightness(60, display_num=2)
