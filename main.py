import json
import sys

grablines = False
timingpointRaw = []

#open .osu file from folder
with open(sys.argv[1], encoding="utf-8") as i:

    #loop
    for line in i.readlines():
        if grablines:
            #create list for each timing point
            tempTimingLine = []

            #split accordingly
            temp = line.strip("\n")
            dataLine = temp.split(',')

            #ignore unnecessary data + append to lineList
            count = 0
            if len(dataLine) != 1:
                if float(dataLine[1]) < 0:
                    continue
                for i in dataLine:
                    if count < 2:
                        tempTimingLine.append(float(i))
                    count = count + 1

                #append to entire timing data
                timingpointRaw.append(tempTimingLine)

        if line == "[TimingPoints]\n" or (line == "\n" and grablines):
            grablines = not grablines 

#temp

#create data
start_offset = float(timingpointRaw[0][0]/1000)
#convert .osu bpm data into .memon-friendly format
bpm_data = []
beat = 0
previousOffset = timingpointRaw[0][0]
previousTiming = timingpointRaw[0][1]
firstTimingPoint = True

#required to keep track in tick form kinda
beat_data = []

for timing_point in timingpointRaw:
    beat = 0
    if firstTimingPoint:
        realBPM = 1 / timing_point[1] * 60000
        bpm_data.append({"beat": beat * 240, "bpm": realBPM})
        firstTimingPoint = False
        previousOffset = timing_point[0]
        previousTiming = timing_point[1]

    else:
        #some calcs made from previous bpm info, add prevoffset at bottom
        realBPM = 1 / timing_point[1] * 60000

        beat_data.append(int(round((timing_point[0] - previousOffset) / previousTiming)))
        for i in beat_data:
            beat = beat + (i * 240)
        bpm_data.append({"beat": beat, "bpm": realBPM})

        previousOffset = timing_point[0]
        previousTiming = timing_point[1]



#buncha buncha json data
json_data = {"version": "1.0.0",
             "metadata": {},
             "timing":   {"offset": start_offset, "bpms": bpm_data},
             #this the good shit yo
             "data":     {"EXT": {"level": 10, "resolution": 240, "notes": [] } }
             }

#format data
json_formatted_str = json.dumps(json_data, indent=4)

#write to output .memon file
with open('output.memon', 'w') as f:
    f.write(json_formatted_str)

print("done!")