# `downdatube` ![GitHub release (latest by date including pre-releases)](https://img.shields.io/github/v/release/shahoob/downdatube?include_prereleases&label=%20&style=flat-square) ![Code Climate maintainability](https://img.shields.io/codeclimate/maintainability/shahoob/downdatube?logo=code-climate&style=flat-square) ![Snyk Vulnerabilities for GitHub Repo](https://img.shields.io/snyk/vulnerabilities/github/shahoob/downdatube?logo=snyk&style=flat-square) ![Lines of code](https://img.shields.io/tokei/lines/github/shahoob/downdatube?style=flat-square)
Yet another YouTube downloader.

## Installation
```shell
pip install -r requirements.txt
```

## Usage
```
Usage: main.py [OPTIONS]

Options:
  -u, --url TEXT
  -i, --itag INTEGER  The itag for using a stream
  --help              Show this message and exit.
```

### Download a video
```
(venv) D:\Quick Projects\downdatube>py main.py --url https://youtu.be/Vp3BS7sBzNc
```
```
Going down da tube...
Seems like that there are 17 streams, It will take a while to fetch all streams. If you have speedy internet, you
may ignore that. Do you want to wait for the picker or find by itag instead? [y/N]:
```
If you say yes:
```

 Which stream?

 * video/mp4 | 1.27 MB | 360p | itag: 18
   video/mp4 | 1.6 MB | 480p | itag: 135
   video/webm | 1.05 MB | 480p | itag: 244
   video/mp4 | 745.5 KB | 480p | itag: 397
   video/mp4 | 830.62 KB | 360p | itag: 134
   video/webm | 575.57 KB | 360p | itag: 243
   video/mp4 | 432.46 KB | 360p | itag: 396
   video/mp4 | 415.17 KB | 240p | itag: 133
   video/webm | 348.4 KB | 240p | itag: 242
   video/mp4 | 220.92 KB | 240p | itag: 395
```
Navigate up and down and <kdb>Enter</kdb> to select
If you said no:
```
Lemme print all the available streams
video/mp4 | 1.27 MB | 360p | itag: 18
video/mp4 | 1.6 MB | 480p | itag: 135
video/webm | 1.05 MB | 480p | itag: 244
video/mp4 | 745.5 KB | 480p | itag: 397
video/mp4 | 830.62 KB | 360p | itag: 134
video/webm | 575.57 KB | 360p | itag: 243
video/mp4 | 432.46 KB | 360p | itag: 396
video/mp4 | 415.17 KB | 240p | itag: 133
video/webm | 348.4 KB | 240p | itag: 242
video/mp4 | 220.92 KB | 240p | itag: 395
video/mp4 | 188.3 KB | 144p | itag: 160
video/webm | 153.99 KB | 144p | itag: 278
video/mp4 | 98.83 KB | 144p | itag: 394
audio/mp4 | 220.62 KB | None | itag: 140
audio/webm | 100.65 KB | None | itag: 249
audio/webm | 147.34 KB | None | itag: 250
audio/webm | 279.35 KB | None | itag: 251
Which itag?: 
```
Then after choosing a stream:
```
video/mp4 | 1.6 MB | 480p | itag: 135
Downloading...
100%|#######################################################################################|  1.2 MiB/s  1.9 MiB
```