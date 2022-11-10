"""This module contains the main logic for yt_downloader."""
# Standard library imports
from typing import Optional, Union
import re
from pathlib import Path
# Third-party imports
import pytube.extract
from pytube import YouTube, Playlist
from pytube.exceptions import RegexMatchError
from halo import Halo
# Local imports
from yt_downloader.validation import (try_except_playlist,
                                      try_except_youtube,
                                      try_except_playlist_title_url)


def create_folder_chl_name(name: str) -> Union[str, None]:
    folder_chl_name = Path(f"{Path.cwd()}/{name}")
    try:
        folder_chl_name.mkdir()
        return str(folder_chl_name)
    except FileExistsError as exc:
        print(exc)
        exit(8)


def extractor_of_channel_name(url: str) -> Union[str, None]:
    """Adding this function as pytube.extract.channel_name doesn't supports
    all patterns """
    # TODO should I use contexlib.supress?
    try:
        chl_name = pytube.extract.channel_name(url)
        return chl_name
    except RegexMatchError:
        pass
    try:
        pattern = re.compile(r'channel=.*')
        match = pattern.search(url)
        chl_name = re.sub('channel=', "", match[0])
    except TypeError:
        print("Channel name was not found in the url!")

    if chl_name is None:
        exit(9)
    else:
        return chl_name


def download_single_video(url: str, target: Optional[str],
                          create_folder=None) -> None:
    """When providing urls for single videos. The video can be saved in the
     current working directory, in a specified target directory or a directory
     can be created by using the channel name of the downloaded video"""
    # Tests correctness of url and creates YouTube obj.
    you_tube = try_except_youtube(url)

    spinner = Halo(text=f'Downloading: {you_tube.title}', spinner='dots')
    spinner.start()

    video = you_tube.streams.get_highest_resolution()
    # If the user wants to create a new folder(based on the channel name)
    # where the video will be saved
    if create_folder:
        if chl_name := extractor_of_channel_name(url):
            folder = create_folder_chl_name(chl_name)
            video.download(folder)
    # If the user indicates where to save the video
    elif target:
        video.download(target)
    # If the user wants to save the video in the current directory
    else:
        video.download()
    spinner.stop()
    print("Downloading finished!")


def download_full_playlist(url: str, target: Optional[str]) -> None:
    """When providing url for a playlist. The playlist can be saved in the
    current working directory or in a specified target directory"""
    # Tests correctness of url and creates list[YouTube]
    yt_playlist = try_except_playlist(url)

    spinner = Halo(text=f'Downloading: {Playlist(url).title}', spinner='dots')
    spinner.start()

    # If the user indicates where to save the playlist
    if target:
        [video.streams.get_highest_resolution().download(target) for video in
         yt_playlist]
    # If the user wants to save the playlist in the current directory
    else:
        # Creating folder name with the playlist name
        folder_playlist = str(Path(f"{Path.cwd()}/{Playlist(url).title}"))

        [video.streams.get_highest_resolution().download(folder_playlist) for
         video in yt_playlist]

    spinner.stop()

    print("Downloading finished!")


def playlist_title_url(url: str) -> list:
    """Allows to download information like title, availability of a playlist
    videos and they respective links"""
    # Tests correctness of url
    yt_url = try_except_playlist_title_url(url)

    spinner = Halo(text=f'Downloading titles and links for '
                        f'{Playlist(url).title}', spinner='dots')
    spinner.start()

    titles_links = []
    video_links = Playlist(yt_url).video_urls
    for link in video_links:
        video_title = YouTube(link).title
        video_ck_aval = YouTube(link).check_availability()
        if video_ck_aval is None:
            video_ck_aval = "ok"
        # TODO why this is not working with from ritch import print in
        #  __main__.py? hyperlink = f"[link={link}]{video_title}[/link]"
        video_title_link = f"{video_title}: {link}. Availability: " \
                           f"{video_ck_aval}"
        titles_links.append(video_title_link)

    spinner.stop()

    return titles_links
