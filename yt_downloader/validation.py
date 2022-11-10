"""This module contains validation checks that return valid objects
processed in yt_dl.py """
# Standard library imports
import requests
# Third-party imports
from pytube import YouTube, Playlist, exceptions
from halo import Halo


def try_except_youtube(url: str) -> YouTube:
    """Validation for single videos"""
    # Checking the url ConnectionError and InvalidURL
    url = try_except_url(url)

    spinner = Halo(text='Testing...', spinner='dots')
    spinner.start()
    # Checking availability of the requested video
    try:
        youtube = YouTube(url)
    except exceptions.VideoUnavailable:
        print(f'Video {youtube.title} is unavailable.')
        exit(1)
    # Extra check for typos in url, I didn't meet this type of error while
    # working with Playlist object, this is wy I didn't included this exception
    # in other try-except functions
    except exceptions.RegexMatchError:
        print('Are you sure the link is ok?')
        exit(2)

    spinner.stop()

    return youtube


def try_except_playlist(url: str) -> list[YouTube]:
    """Validation for playlist"""
    # Checking if the url(ConnectionError and InvalidURL) and Playlist(
    # ).title is ok
    url_check = try_except_playlist_title_url(url)

    spinner = Halo(text='Testing...', spinner='dots')
    spinner.start()

    try:
        playlist_to_check = Playlist(url_check)
        playlist_to_return = []
        for url in playlist_to_check.video_urls:
            # Checking availability of the videos from playlist
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

    if playlist_to_return is None:
        print("No videos were found")
        exit(7)

    return playlist_to_return


def try_except_playlist_title_url(url: str) -> str:
    """Validation of the title of the playlist"""
    # Checking the url ConnectionError and InvalidURL
    url = try_except_url(url)

    spinner = Halo(text='Testing...', spinner='dots')
    spinner.start()

    try:
        # sometimes if the url error is connected to the title it can result
        # in a KeyError: sidebar, here I'm checking if .title is ok
        title_check = Playlist(url).title
    except KeyError:
        print("Are you sure the link is ok?")
        exit(6)

    spinner.stop()

    return url


def try_except_url(url: str) -> str:
    """Validation of url"""
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



