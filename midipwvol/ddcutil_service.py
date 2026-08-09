import subprocess
import re

class DdcutilService:
    """Control monitor brightness via ddcutil CLI"""

    def __init__(self):
        self.vcp_code = "0x10"  # Brightness

    def get_brightness(self, display_num=1):
        """Get current brightness (0-100)"""
        try:
            result = subprocess.run(
                ["ddcutil", "getvcp", self.vcp_code, "--display", str(display_num)],
                capture_output=True,
                text=True,
                check=True
            )
            # Parse output like: "current value =    30, max value =   100"
            match = re.search(r"current value\s*=\s*(\d+)", result.stdout)
            if match:
                return int(match.group(1))
            return None
        except subprocess.CalledProcessError as e:
            print(f"Error getting brightness: {e.stderr}")
            return None


    def set_brightness(self, value, display_num=1):
        """Set brightness (0-100)"""
        try:
            subprocess.run(
                ["ddcutil", "setvcp", self.vcp_code, str(int(value)), "--display", str(display_num)],
                check=True,
                capture_output=True
            )
            return True
        except subprocess.CalledProcessError as e:
            print(f"Error setting brightness: {e.stderr}")
            return False

    def normalize_midi_to_brightness(self, midi_value):
        """Convert MIDI 0-127 to brightness 0-100"""
        return int((midi_value / 127) * 100)

    def set_brightness_from_midi(self, midi_value, display_num=1):
        """Set brightness from MIDI value (0-127)"""
        brightness = self.normalize_midi_to_brightness(midi_value)
        return self.set_brightness(brightness, display_num)
