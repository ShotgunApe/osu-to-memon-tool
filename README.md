# osu-to-memon-tool
Convert timing points found in .osu files into .memon for charting purposes

## Usage:
VERY UNTESTED, most definitely wont work with every beatmap. You'll have better luck with beatmaps whose timing points are snapped to the previous timing point.

- Install python3
- Run cmd: `python3 osu-memon.py [-h] [-r RESOLUTION] [-n NAME] PATH`

Will produce 1.0.0 .memon file in /conversions. Afterward you'll need to add .ogg file to chart folder in F.E.I.S.

## Todo:
- Fix math

- Do audio stuff automatically

- GUI?

## Resources:
https://github.com/Stepland/memon

Thanks to [Stepland](https://github.com/Stepland) for creating F.E.I.S. and [CCPupp](https://github.com/CCPupp) for helping sift through osu file formatting with me
