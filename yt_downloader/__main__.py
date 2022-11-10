# Standard library imports
import argparse
import sys
# Local imports
from yt_downloader.yt_dl import (download_single_video, download_full_playlist,
                                 playlist_title_url)


# TODO runt linter or something
def parse_args():
    parser = argparse.ArgumentParser(
        description="youtube videos downloader")

    parser.add_argument("-v", "--video", type=str, help="url for the video")

    parser.add_argument("-p", "--playlist", type=str,
                        help="url for the playlist")

    parser.add_argument("-pi", "--playlistInfo", type=str,
                        help="""This flag allows to download information 
                        like title, availability of a playlist videos and 
                        they respective links""")

    parser.add_argument("-t", "--target", type=str,
                        help="""The output directory for the downloaded 
                        stream. Default is current working directory""")

    parser.add_argument("-nd", "--newDirectory", help="""If you want to 
    create a new directory named as the channel where the video will be 
    saved""", action="store_true")

    # this prevent to jump to the inputs in main() if all arg are omitted
    if len(sys.argv) == 1:
        parser.print_usage()
        exit(0)

    return parser.parse_args()


def main():
    args = parse_args()

    if args.video:
        download_single_video(args.video, args.target, args.newDirectory)
    if args.playlist:
        download_full_playlist(args.playlist, args.target)
    if args.playlistInfo:
        playlist_info = playlist_title_url(args.playlistInfo)
        for video_info in playlist_info:
            print(video_info)


if __name__ == "__main__":
    main()
