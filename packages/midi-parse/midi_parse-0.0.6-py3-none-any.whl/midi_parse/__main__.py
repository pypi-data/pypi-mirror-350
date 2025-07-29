import time
import sys

import tinysoundfont # type: ignore
from .midi_parse import *

fn = input("your midi file: ")
if fn.startswith("& "): fn = fn[2:]
if fn.startswith("'") and fn.endswith("'"): fn = fn[1:-1]
if fn.startswith("\"") and fn.endswith("\""): fn = fn[1:-1]

mid = MidiFile(open(fn, "rb").read())
sf2 = input("your sf2 file: ") if "--sf" not in sys.argv else sys.argv[sys.argv.index("--sf") + 1]
synth = tinysoundfont.Synth(-12)
sfid = synth.sfload(sf2)
synth.program_select(0, sfid, 0, 0)
synth.start()

keymap: dict[int, bool] = {}
more_delta = 0.0
for msg in mid.play():
    dt = msg["global_sec_delta"] - more_delta
    time.sleep(max(dt, 0.0))
    t = time.perf_counter()
    print(f"\rnow time: {msg["sec_time"]:.2f}s / {mid.second_length:.2f}s", end="")
    
    match msg["type"]:
        case "program_change":
            synth.program_change(msg["channel"], msg["program_number"])
        
        case "controller_change":
            synth.control_change(msg["channel"], msg["controller_number"], msg["controller_value"])
                
        case "note_on":
            keyhash = hash((msg["channel"], msg["note"]))
            if keymap.get(keyhash, False): synth.noteoff(msg["channel"], msg["note"])
            else: keymap[keyhash] = True
            synth.noteon(msg["channel"], msg["note"], msg["velocity"])
            
        case "note_off":
            keyhash = hash((msg["channel"], msg["note"]))
            if keymap.get(keyhash, False):
                synth.noteoff(msg["channel"], msg["note"])
                keymap[keyhash] = False
            
    more_delta = time.perf_counter() - t

time.sleep(5.0)
synth.stop()
