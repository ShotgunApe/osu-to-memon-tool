import json
import sys

grablines = False
timingpointRaw = []

#open .osu file from folder and read timing points
with open(sys.argv[1], encoding="utf-8") as i:

    for line in i.readlines():

        #only get lines from timing points section of .osu
        if grablines:

            #create list for each timing point
            tempTimingLine = []

            #split accordingly
            temp = line.strip("\n")
            dataLine = temp.split(',')

            #ignore unnecessary data + append to tempTimingLine
            count = 0
            if len(dataLine) != 1:
                if float(dataLine[1]) < 0:
                    continue
                for i in dataLine:
                    if count < 2:
                        tempTimingLine.append(float(i))
                    count = count + 1

                #append to timing data
                timingpointRaw.append(tempTimingLine)

        #check to read .osu file in correct position
        if line == "[TimingPoints]\n" or (line == "\n" and grablines):
            grablines = not grablines 

#create data convert .osu bpm data into .memon-friendly format
#keeps track of offset -> beat conv.
beat_data = []

#bpm_data is the final timing data insert into .memon file
bpm_data = []

start_offset = float(timingpointRaw[0][0]/1000)
previousOffset = timingpointRaw[0][0]
previousTiming = timingpointRaw[0][1]
firstTimingPoint = True

for timing_point in timingpointRaw:
    #use symbolic time array to keep track of beat
    beat = [0,0,1]

    if firstTimingPoint:
        #calculate bpm
        realBPM = 1 / timing_point[1] * 60000

        #first timing point has first beat at 0
        bpm_data.append({"beat": [0,0,1], "bpm": realBPM})
        firstTimingPoint = False

        #set previous offset and previous timing
        previousOffset = timing_point[0]
        previousTiming = timing_point[1]

    else:
        #calculate BPM
        realBPM = 1 / timing_point[1] * 60000

        #keep track of "beat data" - position in .memon file where next timing point should be placed
        beat_data.append((timing_point[0] - previousOffset) / previousTiming)
        for i in beat_data:
            beat[0] = beat[0] + round(i)
        bpm_data.append({"beat": beat, "bpm": realBPM})

        #save previous offset/timing for beat position
        previousOffset = timing_point[0]
        previousTiming = timing_point[1]

#.memon json formatting
json_data = {"version": "1.0.0",
             "metadata": {},
             "timing":   {"offset": start_offset, "bpms": bpm_data},
             "data":     {"EXT": {"level": 10, "resolution": 240, "notes": [] } }
             }

#create formatted string
json_formatted_str = json.dumps(json_data, indent=4)

#write to output .memon file
with open('output.memon', 'w') as f:
    f.write(json_formatted_str)

print("done!")