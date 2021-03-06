import jack
import queue
import time
import PySimpleGUI as sg

MIDICHANNEL = 1

padconf = {
    (0,0):{"note":36,"vel":127},
    (1,0):{"note":38,"vel":127},
    (0,1):{"note":44,"vel":127},
    (1,1):{"note":46,"vel":127}
}

# Open the connection to jack-midi
client = jack.Client('MIDI-Controller')
outport = client.midi_outports.register('output')
midi_msg_q = queue.Queue()

@client.set_process_callback
def process(frames):
    global midi_msg_q
    outport.clear_buffer()
    try:
        while True:
            midi_msg = midi_msg_q.get(block=False)
            outport.write_midi_event(0, midi_msg)
    except queue.Empty:
        pass

client.activate()

def midi_note(channel, midi_note,vel):
    midi_msg_q.put((0x90 | channel, midi_note, vel)) #NOTE ON
    midi_msg_q.put((0x80 | channel, midi_note, 0))   #NOTE OFF


#PySimpleGUI
layout = [[sg.B(' ', size=(12,6), key=(i,j)) for i in range(2)] for j in range(2)]
window = sg.Window('Midi Controller', layout)

# run loop
while True:
    event, values = window.read()
    if event == sg.WIN_CLOSED or event == 'Exit':
        break
    try:
        print(event,padconf[event])
        midi_note(MIDICHANNEL,padconf[event]["note"],padconf[event]["vel"])
    except:
        pass

window.close()
        
