# yt-downloader
A command line interface tool written in python for downloading YouTube videos.
___
## Usage
````
usage: yt-downloader [-h] [-v VIDEO] [-p PLAYLIST] [-pi PLAYLISTINFO] [-t TARGET] [-nd]

youtube videos downloader

optional arguments:
  -h, --help            show this help message and exit
  -v VIDEO, --video VIDEO
                        url for the video
  -p PLAYLIST, --playlist PLAYLIST
                        url for the playlist, use quotation marks 'url'
  -pi PLAYLISTINFO, --playlistInfo PLAYLISTINFO
                        This flag allows to download information like title, availability of a
                        playlist videos and they respective links
  -t TARGET, --target TARGET
                        The output directory for the downloaded stream. Default is current
                        working directory
  -nd, --newDirectory   If you want to create a new directory named as the channel where the
                        video will be saved
````
___
## Installation
Build from source:  
For Linux:  
Along with >=Python3.8 you need to have Poetry installed, then just run the command:
`poetry build`  
to build the project. The package will be saved to `dist` folder, from where you can install it with `pip install filename`  
For Windows:  
Download the repository and on `cmd ` run `pip install path to local repository`
___
## Contributing
Contributions are welcomed, always fun to collaborate:)  
Some rules:

Please focus hard on the naming of functions, classes, and variables.  
Help your reader by using descriptive names that can help you to remove redundant comments.  
Expand acronyms because `dfp()` is hard to understand but `download_full_playlist()` is not.
Use type hints for your functions.
___
