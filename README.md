<h1 align="center">fzdown-api</h1>

<p align="center">
<a href="#"><img alt="Python version" src="https://img.shields.io/pypi/pyversions/fdown-api"/></a>
<a href="https://github.com/Simatwa/fdown-api/actions/workflows/python-test.yml"><img src="https://github.com/Simatwa/fdown-api/actions/workflows/python-test.yml/badge.svg" alt="Python Test"/></a>
<a href="LICENSE"><img alt="License" src="https://img.shields.io/static/v1?logo=MIT&color=Blue&message=MIT&label=License"/></a>
<a href="https://pypi.org/project/fdown-api"><img alt="PyPi" src="https://img.shields.io/pypi/v/fdown-api"></a>
<a href="https://github.com/Simatwa/fdown-api/releases"><img src="https://img.shields.io/github/v/release/Simatwa/fdown-api?label=Release&logo=github" alt="Latest release"></img></a>
<a href="https://github.com/Simatwa/fdown-api/releases"><img src="https://img.shields.io/github/release-date/Simatwa/fdown-api?label=Release date&logo=github" alt="release date"></img></a>
<a href="https://github.com/psf/black"><img alt="Black" src="https://img.shields.io/badge/code%20style-black-000000.svg"/></a>
<a href="https://github.com/Simatwa/fdown-api/actions/workflows/python-publish.yml"><img src="https://github.com/Simatwa/fdown-api/actions/workflows/python-publish.yml/badge.svg" alt="Python-publish"/></a>
<a href="https://pepy.tech/project/fdown-api"><img src="https://static.pepy.tech/personalized-badge/fdown-api?period=total&units=international_system&left_color=grey&right_color=blue&left_text=Downloads" alt="Downloads"></a>
<a href="https://github.com/Simatwa/fdown-api/releases/latest"><img src="https://img.shields.io/github/downloads/Simatwa/fdown-api/total?label=Asset%20Downloads&color=success" alt="Downloads"></img></a>
<a href="https://hits.seeyoufarm.com"><img src="https://hits.seeyoufarm.com/api/count/incr/badge.svg?url=https%3A%2F%2Fgithub.com/Simatwa/fdown-api"/></a>
</p>

Download facebook videos with ease.

## Installation

```sh
$ pip install fdown-api[cli]
```

## Usage
 
### Developers

```python
from fdown_api import Fdown

f = Fdown()
video_links = f.get_links(
    "https://www.facebook.com/reel/8365833600105776\?mibextid\=rS40aB7S9Ucbxw6v"
)
saved_to = f.download_video(video_links)
print(saved_to)
# Will show download progress
"""
3 MB ███████████████████                          43%|
"""
```

### CLI

`$ python -m fdown_api <facebook-video-url>`

<details>
<summary>
<code>$ fdown --help</code>

</summary>

```
usage: fdown [-h] [-d PATH] [-o PATH] [-q normal|hd] [-t TIMEOUT]
             [-c chunk-size] [--resume] [--quiet] [--version]
             url

Download Facebook videos seamlessly.

positional arguments:
  url                   Link to the target facebook video

options:
  -h, --help            show this help message and exit
  -d, --dir PATH        Directory for saving the video to -
                        /home/smartwa/git/smartwa/fdown-api
  -o, --output PATH     Filename under which to save the video to - random
  -q, --quality normal|hd
                        Video download quality - hd
  -t, --timeout TIMEOUT
                        Http request timeout in seconds - 20
  -c, --chunk-size chunk-size
                        Chunk-size for downloading files in KB - 512
  --resume              Resume an incomplete download - False
  --quiet               Do not stdout any informational messages - False
  --version             show program's version number and exit

This script has no official relation with fdown.net.
```
</details>

# Disclaimer

This repository contains an unofficial Python wrapper for fdown.net. It is not affiliated with or endorsed by the official fdown.net service or its developers.
This wrapper is intended for personal use and education only. The author(s) of this repository are not responsible for any misuse of this code or any damages caused by its use.