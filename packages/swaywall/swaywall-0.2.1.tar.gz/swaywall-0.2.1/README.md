## Swaywall

An intelligent wallpaper switcher for `swaywm`.

+ Sets a random wallpaper from a given directory
+ Remembers previous selections:
	- Never repeats a wallpaper until the entire catalogue has been cycled through
	- Can restore the latest selection (useful on `swaywm` start)

## Installation

`swaywall` is packaged on [PyPi](https://pypi.org/project/swaywall) and can be installed using, for example, [`pipx`](https://pipx.pypa.io/stable/):

+ `pipx install swaywall`

## Usage

```
usage: swaywall [-h] [-r] [-e EXT [EXT ...]] dir

Intelligent wallpaper switcher for swaywm

positional arguments:
  dir                   path to wallpaper directory

options:
  -h, --help            show this help message and exit
  -r, --restore         restore latest wallpaper
  -e, --extensions EXT [EXT ...]
                        image file extensions to look for (default: png jpg jpeg)
```
