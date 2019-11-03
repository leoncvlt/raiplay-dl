Python downloader for the Italian streaming platform [RaiPlay](https://www.raiplay.it/)

# Installation / Requirements

`pip install -r requirements.txt`

RaiPlay serves video via [HLS](https://en.wikipedia.org/wiki/HTTP_Live_Streaming) streams. [youtube-dl](https://ytdl-org.github.io/youtube-dl/index.html) is used to process and download the m3u8 playlist files for them.

## Usage

```text
usage: raiplay-dl [-h] [-d download_directory] url

positional arguments:
  url                   URL of the content to download

optional arguments:
  -d download_directory
                        Directory to download content to
```

The URL can be the url of a single episode / film (e.g. `https://www.raiplay.it/video/2019/10/Aspettando-VivaRaiPlay-Ep-1-14b79f55-1c75-44ab-b861-281615b94636.htmll`), or a whole series (e.g. `https://www.raiplay.it/programmi/vivaraiplay`), in which case all seasons / episodes will be downloaded. Downloaded content will be organised in folders based on the content's show name and seasons.

Although (free) registration to RaiPlay is required to watch content on the platform, you can grab the required URLs for download without making an account, nor `raiplay-dl` requires authentication details to download.