# Standard library imports
import argparse
import sys
# Local imports
from yt_downloader.yt_dl import (download_single_video, download_full_playlist,
                                 playlist_title_url)
from yt_downloader.validation import (_try_except_playlist,
                                      _try_except_youtube,
                                      _try_except_playlist_title_url)


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
                        help="info")

    parser.add_argument("-t", "--target", type=str,
                        help="The output directory for the downloaded stream. "
                             "Default is current working directory")
    # TODO czy target to dobra nazwa
    return parser.parse_args()


def main(argv):
    args = parse_args(argv)

    if args.video:
        yt_video = _try_except_youtube(args.video)
        download_single_video(yt_video, args.target)
    if args.playlist:
        yt_playlist = _try_except_playlist(args.playlist)
        download_full_playlist(yt_playlist, args.target, args.playlist)
    if args.info:
        yt_url = _try_except_playlist_title_url(args.info)
        playlist_info = playlist_title_url(yt_url)
        for i in playlist_info:
            print(i)


if __name__ == "__main__":
    main(sys.argv[1:])
