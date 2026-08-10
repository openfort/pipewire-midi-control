# pipewire-midi-control 🎚🎛️ → 🔈🔉🔊

Tool to map MIDI messages to the audio volume of individual PipeWire nodes and devices.

Current status: Early development, not very polished. But I'm already using it daily with Behringer X-TOUCH MINI.

Goals:

* Use MIDI CC messages to change individual volume levels in PipeWire.
    * Should support any device/node/port/whatever-it-is-called.
    * Should also support applications.
* Also use them to change the display brightness.
    * Using `ddcutil` for external displays.
* Also allow changing the default audio device (both for playback and for recording).
* Also allow changing the profile of an audio device.
* Also allow arbitrary commands.
* Any MIDI message should work. CC messages, note on/off.

## TODO

* [ ] Write a better README file.
    * Explain what this tool does, what it does not, and what are the alternative tools.
    * Step-by-step installation instructions.
    * Some configuration examples.
* [x] Write a nice `set_volume` function that...
    * Accepts absolute amounts.
    * Allows setting `mute`.
    * Allows per-channel changes.
* [ ] Write a nice `change_volume` function that...
    * Accepts relative amounts.
    * Has a maximum limit for relative amounts.
    * Allows toggling `mute`.
    * Allows per-channel changes.
* [ ] Get the focused Window on the Desktop.
    * Change volume of focused Window.
    * Assign focused Window to midi controls.
* [x] Hard-code changing the volume from a MIDI CC event.
* [ ] Write a nice function to change the default input/output device.
* [ ] Write a nice function to change the profile of a device.
* [ ] Allow changing the volume/mute of the default device.
* [ ] Let the user (i.e. the config file) decide if a MIDI device should be auto-connected to this tool.
* [ ] Auto-connect MIDI devices when they get hot-plugged.
* [ ] Filter for MIDI channel to allow mulitple MIDI devices.
* [ ] Send values back to the MIDI device
    * [ ] Send volume changes. (Requires figuring out how to detect volume changes.)
    * [ ] Send brightness/contrast VDU changes. (Requires receiving signals from ddcutil-session, not sure if it is possible.
    * [ ] Buy or borrow a MIDI device that I can test. Maybe I should just connect to my Akai Play Mini and map it to one of the knobs.
* [ ] Write a lot of docstrings. Documentation is important.
* [ ] Write a lot of unit tests, possibly as doctests.
* [x] Figure out a nice configuration format. Or maybe just a simple API so that users can write their own code.
* [x] Write a function to send updates to `ddcutil-cli`.
* [ ] Write a help function. Well, just use `argparse`. But write a parameter that prints out:
    * All the currently available MIDI devices/ports.
    * All the audio devices/nodes/etc.
    * Any significant changes detected.
    * Incoming MIDI messages.
    * Heck, this is just a `--verbose` mode!

## Further links

* forked from [denilsonsa/midi-pipewire-volume](https://github.com/denilsonsa/midi-pipewire-volume)
* [PipeWire](https://pipewire.org/)
    * [How to change the volume in PipeWire](https://gitlab.freedesktop.org/pipewire/pipewire/-/wikis/Migrate-PulseAudio#sinksource-port-volumemuteport-latency) (TL;DR: it's complicated)
    * [Desire for official PipeWire Python bindings](https://gitlab.freedesktop.org/pipewire/pipewire/-/issues/1654)
* [WirePlumber](https://pipewire.pages.freedesktop.org/wireplumber/)
    * [Getting a list of devices and applications, using `pw-dump` and `jq`](https://github.com/PipeWire/wireplumber/blob/0.5.1/src/tools/shell-completion/wpctl.zsh#L8-L20)
    * [Keyboard volume control using `wpctl`](https://wiki.archlinux.org/title/WirePlumber#Keyboard_volume_control)
    * [The source code of `wpctl set-volume`](https://github.com/PipeWire/wireplumber/blob/master/modules/module-mixer-api.c)
* Potentially related projects:
    * [deej](https://github.com/omriharel/deej) - Open-source hardware volume mixer. Requires custom hardware recognized as a serial interface, and a custom daemon written in Go. It's almost the same objective as this/my project, but my project aims to work with already existing MIDI devices.
    * [midi2input](https://gitlab.com/enetheru/midi2input) - Uses Lua and C++ to convert MIDI to arbitrary commands. Looks very versatile and more powerful than my project, but also more complicated.
    * [AV-MidiMacros](https://github.com/Avante-Vangard/AV-MidiMacros) - Shell script and a bunch of CSV files. Might be useful to someone.
    * [Translating MIDI input into computer keystrokes on Linux?](https://superuser.com/questions/1170136/translating-midi-input-into-computer-keystrokes-on-linux) - Has an ad-hoc solution using `aseqdump` and `xdotool`.
    * [Regulate system volume with midi controller](https://unix.stackexchange.com/questions/297449/regulate-system-volume-with-midi-controller)
