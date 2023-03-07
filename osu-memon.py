import json
import argparse

#command line options
def parse_args():
    #init argparse
    parser = argparse.ArgumentParser(description = "osu-to-memon-tool options", formatter_class = argparse.ArgumentDefaultsHelpFormatter)

    # ~options~
    parser.add_argument('-r', type=int, help = 'sets number of ticks in a beat for all the notes in a chart', default=240, metavar='RESOLUTION')
    parser.add_argument('-n', help = 'name of output file to be made', default='[filename].memon', metavar='NAME')
    parser.add_argument('PATH', help = 'path to .osu file')

    argument = parser.parse_args()

    return argument

#convert .osu timing data -> .memon timing data
def convert_timing_data(timing_data):

    #keeps track of offset -> beat conv.
    beat_data = []

    #bpm_data is the final timing data insert into .memon file
    bpm_data = []

    previousOffset = timingpointRaw[0][0]
    previousTiming = timingpointRaw[0][1]
    firstTimingPoint = True

    for timing_point in timing_data:
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

            #filter rounding error
            for i in beat_data:
                if (i % 1) > 0.99 or (i % 1) < 0.01:
                    beat[0] = beat[0] + round(i)
                else:
                    beat[0] = beat[0] + i

            #calculate other beat information from decimal of beat[0]
            tempBeat = beat[0] % 1

            #set beat values
            beat[0] = round(beat[0])
            beat[1] = handle_remainder(tempBeat)[0]
            beat[2] = handle_remainder(tempBeat)[1]
            bpm_data.append({"beat": beat, "bpm": realBPM})

            #save previous offset/timing for beat position
            previousOffset = timing_point[0]
            previousTiming = timing_point[1]
    
    return bpm_data

#handle remainder with rounding error
def handle_remainder(remainder):
    remainder = remainder * 100
    if remainder > 97:
        return [0,100]
    return [int(remainder),100]

#start here
if __name__ == '__main__':

    #raw timing data from .osu file
    timingpointRaw = []

    with open(parse_args().PATH, encoding = "utf-8") as file:
        #check whether to grab lines in .osu file
        grablines = False

        for line in file.readlines():
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

    #audio offset
    start_offset = float(timingpointRaw[0][0]/1000)

    #.memon json formatting
    json_data = {"version": "1.0.0",
                 "metadata": {},
                 "timing":   {"offset": start_offset, "bpms": convert_timing_data(timingpointRaw)},
                 "data":     {"EXT": {"level": 10, "resolution": parse_args().r, "notes": [] } }
                 }

    #create formatted string
    json_formatted_str = json.dumps(json_data, indent=4)

    filename = ""

    #check which name to use
    if parse_args().n != '[filename].memon':
        filename = parse_args().n + '.memon'
    else:
        filename = parse_args().PATH.removesuffix('.osu').removeprefix('.\\')+'.memon'

    #write to output .memon file
    with open('conversions/'+filename, 'w') as f:
        f.write(json_formatted_str)

    print("done!")