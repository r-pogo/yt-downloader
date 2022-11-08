# Standard library imports
import argparse
import sys
# Local imports
from yt_downloader.yt_dl import (download_single_video, download_full_playlist,
                                 playlist_title_url)


def parse_args(args):
    # TODO skonczyc i sprawdzic opisy
    parser = argparse.ArgumentParser(
        description="youtube downloader")
    # if all arg are omitted displays simple usage
    if not args:
        parser.print_help()
        exit(0)

    parser.add_argument("-v", "--video", type=str, help="url for the video")

    parser.add_argument("-p", "--playlist", type=str,
                        help="url for the playlist")

    parser.add_argument("-i", "--info", type=str,
                        help="info") # TODO tu opisac ze to url do info?

    parser.add_argument("-t", "--target", type=str,
                        help="The output directory for the downloaded stream."
                             "Default is current working directory")
    parser.add_argument("-nd", "--newDirectory", help="""if you want to create
                                                      a new dierctory named
                                                      as the channel where
                                                      to save your videos""",
                        action="store_true")
    # TODO czy target to dobra nazwa
    return parser.parse_args()


def main(argv):
    args = parse_args(argv)

    if args.video:
        download_single_video(args.video, args.target, args.newDirectory)
    if args.playlist:
        download_full_playlist(args.playlist, args.target)
    if args.info:
        playlist_info = playlist_title_url(args.info)
        for video_info in playlist_info:
            print(video_info)


if __name__ == "__main__":
    main(sys.argv[1:])
