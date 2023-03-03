import json
import sys

import ast

grablines = False
timingpointRaw = []

#open .osu file from folder
with open(sys.argv[1], "r") as i:

    #loop
    for line in i.readlines():
        if grablines:
            #this is dumb
            temp = line.strip("\n")
            res = temp.split(',')
            timingpointRaw.append(res)

        if line == "[TimingPoints]\n" or (line == "\n" and grablines):
            #something to grab data ig
            print("good")
            grablines = not grablines 

print(timingpointRaw)
#temp
start_offset = 3.2

#create data
#convert .osu bpm data into .memon-friendly format

bpm_data = {}

#buncha buncha json data
json_data = {"version": "1.0.0",
             "metadata": {},
             "timing":   {"offset": start_offset},
             #this the good shit yo
             "data":     {"EXT": {"timing": {"offset": start_offset, "bpms": [bpm_data] }, "notes": [] } }
             }

#format data
json_formatted_str = json.dumps(json_data, indent=4)

#write to output .memon file
with open('output.memon', 'w') as f:
    f.write(json_formatted_str)