import json
import argparse

HIGH_ROUNDING_CUTOFF = 0.99
LOW_ROUNDING_CUTOFF = 0.01
BPM_CALCULATION_CONSTANT = 60000
REMAINDER_CUTOFF = 97

#command line options
def parse_args():
    #init argparse
    parser = argparse.ArgumentParser(description = "osu-to-memon-tool options", formatter_class = argparse.ArgumentDefaultsHelpFormatter)

    # ~options~
    parser.add_argument('-r', type=int, help = 'sets number of ticks in a beat for all the notes in a chart', default=240, metavar='RESOLUTION')
    parser.add_argument('-n', help = 'name of output file to be made', default='[file_name].memon', metavar='NAME')
    parser.add_argument('PATH', help = 'path to .osu file')

    argument = parser.parse_args()

    return argument

#convert .osu timing data -> .memon timing data
def convert_timing_data(timing_data):

    #keeps track of offset -> beat conv.
    beat_data = []

    #bpm_data is the final timing data insert into .memon file
    bpm_data = []

    previous_offset = timingpoint_raw[0][0]
    previous_timing = timingpoint_raw[0][1]
    first_timing_point = True

    for timing_point in timing_data:
        #use symbolic time array to keep track of beat
        beat = [0,0,1]

        if first_timing_point:
            #calculate bpm
            real_bpm = 1 / timing_point[1] * BPM_CALCULATION_CONSTANT

            #first timing point has first beat at 0
            bpm_data.append({"beat": [0,0,1], "bpm": real_bpm})
            first_timing_point = False

            #set previous offset and previous timing
            previous_offset = timing_point[0]
            previous_timing = timing_point[1]

        else:
            #calculate BPM
            real_bpm = 1 / timing_point[1] * BPM_CALCULATION_CONSTANT

            #keep track of "beat data" - position in .memon file where next timing point should be placed
            beat_data.append((timing_point[0] - previous_offset) / previous_timing)

            #filter rounding error
            for i in beat_data:
                if (i % 1) > HIGH_ROUNDING_CUTOFF or (i % 1) < LOW_ROUNDING_CUTOFF:
                    beat[0] = beat[0] + round(i)
                else:
                    beat[0] = beat[0] + i

            #calculate other beat information from decimal of beat[0]
            temp_beat = beat[0] % 1

            #set beat values
            beat[0] = round(beat[0])
            beat[1] = handle_remainder(temp_beat)[0]
            beat[2] = handle_remainder(temp_beat)[1]
            bpm_data.append({"beat": beat, "bpm": real_bpm})

            #save previous offset/timing for beat position
            previous_offset = timing_point[0]
            previous_timing = timing_point[1]
    
    return bpm_data

#handle remainder with rounding error
def handle_remainder(remainder):
    remainder = remainder * 100
    if remainder > REMAINDER_CUTOFF:
        return [0,100]
    return [int(remainder),100]

#start here
if __name__ == '__main__':

    #raw timing data from .osu file
    timingpoint_raw = []

    with open(parse_args().PATH, encoding = "utf-8") as file:
        #check whether to grab lines in .osu file
        grab_lines = False

        for line in file.readlines():
            #only get lines from timing points section of .osu
            if grab_lines:

                #create list for each timing point
                temp_timing_line = []

                #split accordingly
                temp = line.strip("\n")
                data_line = temp.split(',')

                #ignore unnecessary data + append to temp_timing_line
                count = 0
                if len(data_line) != 1:
                    if float(data_line[1]) < 0:
                        continue
                    for i in data_line:
                        if count < 2:
                            temp_timing_line.append(float(i))
                        count = count + 1

                    #append to timing data
                    timingpoint_raw.append(temp_timing_line)

            #check to read .osu file in correct position
            if line == "[TimingPoints]\n" or (line == "\n" and grab_lines):
                grab_lines = not grab_lines 

    #audio offset
    start_offset = float(timingpoint_raw[0][0]/1000)

    #.memon json formatting
    json_data = {"version": "1.0.0",
                 "metadata": {},
                 "timing":   {"offset": start_offset, "bpms": convert_timing_data(timingpoint_raw)},
                 "data":     {"EXT": {"level": 10, "resolution": parse_args().r, "notes": [] } }
                 }

    #create formatted string
    json_formatted_str = json.dumps(json_data, indent=4)

    file_name = ""

    #check which name to use
    if parse_args().n != '[file_name].memon':
        file_name = parse_args().n + '.memon'
    else:
        file_name = parse_args().PATH.removesuffix('.osu').removeprefix('.\\')+'.memon'

    #write to output .memon file
    with open('conversions/'+file_name, 'w') as f:
        f.write(json_formatted_str)

    print("Done!")