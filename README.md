# osu-to-memon-tool
Convert timing points found in .osu files into .memon for charting purposes

# Usage:
VERY UNTESTED, most definitely wont work with every beatmap. You'll have better luck with beatmaps whose timing points are snapped to the previous timing point.

cmd: `python3 main.py "[path_to_file.osu]"`

Will produce output.memon file in 1.0.0 format. Afterward you'll need to add .ogg file to chart folder in F.E.I.S.

# Resources:
https://github.com/Stepland/memon

Thanks to [Stepland](https://github.com/Stepland) for creating F.E.I.S. and [CCPupp](https://github.com/CCPupp) for helping sift through osu file formatting with me
