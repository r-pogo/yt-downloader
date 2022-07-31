# Standard library imports
import requests
# Third-party imports
from pytube import YouTube, Playlist, exceptions
from halo import Halo


def _try_except_youtube(url: str) -> YouTube:
    url = _try_except_url(url)

    spinner = Halo(text='Testing...', spinner='dots')
    spinner.start()

    try:
        youtube = YouTube(url)
    except exceptions.VideoUnavailable:
        print(f'Video {youtube.title} is unavailable.')
        exit(1)
    except exceptions.RegexMatchError:  # extra check for typos in url
        print('Are you sure the link is ok?')
        exit(2)

    spinner.stop()

    return youtube


def _try_except_playlist(url: str) -> list[YouTube]:
    url_check = _try_except_playlist_title_url(url)

    spinner = Halo(text='Testing...', spinner='dots')
    spinner.start()

    try:
        playlist_to_check = Playlist(url_check)
        playlist_to_return = []
        for url in playlist_to_check.video_urls:
            try:
                youtube = YouTube(url)
                playlist_to_return.append(youtube)
            except exceptions.VideoUnavailable:
                print(f'Video {youtube.title} is unavailable, skipping.')
                continue
    except KeyError:  # for eventual KeyError in playlist_to_check
        print("Are you sure the link is ok?")
        exit(3)

    spinner.stop()

    return playlist_to_return


def _try_except_playlist_title_url(url: str) -> str:
    url = _try_except_url(url)

    spinner = Halo(text='Testing...', spinner='dots')
    spinner.start()

    try:
        # sometimes if the url error is connected to the title it can result
        # in a KeyError: sidebar, here I'm checking if .title is ok
        # is a function separated from _try_except_playlist, because i
        # also need to use it for playlist_title_url
        title_check = Playlist(url).title
    except KeyError:
        print("Are you sure the link is ok?")
        exit(6)

    spinner.stop()

    return url


def _try_except_url(url: str) -> str:
    spinner = Halo(text='Testing...', spinner='dots')
    spinner.start()

    try:
        response = requests.get(url)
    except requests.exceptions.ConnectionError as err:
        print(f"Failed to establish a connection: {err}")
        exit(4)
    except requests.exceptions.InvalidURL as err:
        print(err)
        exit(5)

    spinner.stop()

    return url



