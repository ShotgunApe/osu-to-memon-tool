# osu-to-memon-tool
Convert timing points found in .osu files into .memon for charting purposes

## Usage:
VERY UNTESTED, most definitely wont work with every beatmap. You'll have better luck with beatmaps whose timing points are snapped to the previous timing point.

- Install python3
- Run cmd: `python3 osu-memon.py [-h] [-r RESOLUTION] [-n NAME] PATH`
#### Options:
- `-r RESOLUTION`  -   sets number of ticks in a beat for all the notes in a chart (default: 240)
- `-n NAME`        -   name of output file to be made (default: [filename].memon)
- `PATH` is the path to your .osu file

This will produce a 1.0.0 .memon file in /conversions. Afterward you'll need to add .ogg file to chart folder in F.E.I.S.

#### Example: 

`python3 osu-memon.py -r 300 -n "theyaremanycolors" "C:\[path_to_beatmap]\[filename].osu"` produces `theyaremanycolors.memon` with a resolution of 300 ticks

## Todo:
- Fix math

- Do audio stuff automatically

- GUI?

## Resources:
https://github.com/Stepland/memon

Thanks to [Stepland](https://github.com/Stepland) for creating F.E.I.S. and [CCPupp](https://github.com/CCPupp) for helping sift through osu file formatting with me
