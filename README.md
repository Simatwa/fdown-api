# fdown-api
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
    "https://www.facebook.com/reel/916344720334368?mibextid=rS40aB7S9Ucbxw6v"
)
saved_to = f.download_video(video_links)
print(saved_to)

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