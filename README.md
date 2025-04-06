###MIDI Keys
This minimalist program operates for any game or task that may require key presses which correspond to a MIDI sequence. It takes key mappings to particular musical notes, and presses the keys when they are played in the sequence. The syntax takes the following form:

'''
--key=[NOTE], ... : [KEY] ; ... ;
'''

The parser is supported by a robust regular expression and is versatile. It can handle whitespace.

It was originally written for the [Roblox Drum Kit](https://www.roblox.com/catalog/33866728/Drum-Kit), which has the following constraints:
- H - Snare Drum
- N - Bass Drum
- K - Floor Tom
- J - Mid Tom
- U - High Tom
- G - Hi-hat Open
- T - Ride
- Y - Crash
