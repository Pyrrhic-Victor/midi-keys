from argparse import ArgumentParser
from keyboard import press_and_release, add_hotkey
from os.path import join, isfile
from re import fullmatch
from mido import MidiFile
from time import sleep

# Devised a robust regex to recognize proper syntax
# Function to play MIDI file with key mappings
def playMidi(midi: MidiFile, list: list, channel: int):

    # Process each message
    for msg in midi.play():
        print(msg)
        if msg.dict()["channel"] == channel:

            # Attempt to process note specified in message
            try: note = msg.note
            except: continue

            # Press notes cooresponding to map
            for map in list:
                if map[0] == note:
                    if msg.type == "note_on":
                        press_and_release(map[1])

# Main function
if __name__ == "__main__":

    # Initialize argument parser
    parser = ArgumentParser(prog="MIDI Keys",
    description="""Plays the drums in Roblox using a MIDI file. Runs through a
                MIDI file and assigns notes to certain keys that coorespond to
                drum keys.""")

    # File Argument
    parser.add_argument("-f", "--file", type=str, help="The path to the mid file.")

    # Musical key Argument
    parser.add_argument("-k", "--key", type=str,
    help="The musical key(s) to associate with a keyboard key."
         "Usage: --key=[NOTE], ... : [KEY] ; ... ;"
         "Example: --key=64:H;44,45:Y;\tAssociate C6 with S button and E4 and F4 with Y button.")

    # Channel argument
    parser.add_argument("-c", "--channel", type=str,
    help=f"The MIDI channel to catch note occurences at.")

    # Loop argument
    parser.add_argument("-l", "--loop", type=str,
    help="Whether to loop (--loop=y / --loop=n), or for how many times to loop (--loop=4).")

    # Delay argument
    parser.add_argument("-d", "--delay", type=str,
    help="Delay program start by specified number of seconds.")

    # Get arguments
    args = parser.parse_args()
    file = args.file
    key = args.key
    channel = args.channel
    loop = args.loop
    delay = args.delay

    # Process file argument
    if file == None:
        print("Expected --file argument usage")
        exit()
    elif not isfile(file):
        print("Invalid --file path")
        exit()
    else:
        file = join(file)

    # Process key argument
    if key == None:
        print("Expected --key argument usage")
        exit()
    else:
        re_key = r"((([ ]*[\d]{,3}[ ]*[,:][ ]*)*(?<=:)[\w^\d])[ ]*;)*"
        if not fullmatch(re_key, key):
            print("Invalid --key argument")
            exit()

    # Process channel argument
    if channel == None:
        channel = 1
    else:
        channel = int(channel)

    # Process loop argument
    if loop == None:
        loop = 'n'
    else:
        re_loop = r"[ ]*([\d]*|[yn])[ ]*"
        if not fullmatch(re_loop, loop):
            print("Invalid --loop argument")
            exit()

    # Process delay argument
    if delay == None:
        delay = 5
    else:
        delay = abs(int(delay))

    # Process the key assignments into key_arr
    key_arr = []
    for i in range(key.count(';')):
        
        # Segregate assignments based on semicolon, cut observed portion off
        i_key = key[:key.find(';')]
        key = key[key.find(';')+1:]

        # Separate keys and drum assignment
        key_string = i_key.partition(':')[0]
        key_char = i_key.partition(':')[2]

        # Process each key number specified in assignment
        if key_string.count(',') > 0:
            comma_count = key_string.count(',') + 1
            for j in range(comma_count):

                # Separate keys based on usage of comma, cut taken portion off
                if j == comma_count - 1:
                    key_arr.append([int(key_string), key_char])
                else:
                    j_key = key_string[:key_string.find(',')]
                    key_string = key_string[key_string.find(',')+1:]
                    key_arr.append([int(j_key), key_char])
        else:
            key_arr.append([int(key_string), key_char])

    # Load MIDI file
    midi = MidiFile(file)

    # Provide count-down
    for i in range(delay):
        for j in range(3):
            sleep(.25)
            print('.', end='')
        print(f"{delay - i} ", end='')
    print(end='\n')

    # Play MIDI a specified number of times
    if loop == 'n':
        playMidi(midi, key_arr, channel)
        pass
    elif loop == 'y':
        while(True):
            playMidi(midi, key_arr, channel)
            pass
    else:
        for i in range(0, loop):
            playMidi(midi, key_arr, channel)
            pass
