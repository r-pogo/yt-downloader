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


def create_folder_chl_name(name: str):
    p = Path(f"{Path.cwd()}/{name}")
    try:
        p.mkdir()
        return str(p)
    except FileExistsError as exc: #TODO tu jesli mam juz directory to i tak sciagnie plik, ale jak za trzecim razem sprobuje to wylapuje błoad
        print(exc)


def extractor_of_channel_name(url: str) -> Union[str, None]:
    """Adding this function as pytube.extract.channel_name doesn't supports
    all patterns """
    try:
        chl_name = pytube.extract.channel_name(url)
        return chl_name
    except RegexMatchError:
        pass
    try:
        pattern = re.compile(r'channel=.*')
        match = pattern.search(url)
        chl_name = re.sub('channel=', "", match[0])
        return chl_name
    except TypeError:
        print("Channel name was not found in the url! Downloading to the "
              "current directory.")


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
    # where to save the video
    if create_folder:
        if chl_name := extractor_of_channel_name(url):
            folder = create_folder_chl_name(chl_name)
            video.download(folder)
        elif chl_name is None:
            video.download()
    # If the user indicates where to save the video
    elif target:
        video.download(target)
    # If the user wants to save the video in the current directory
    else:
        video.download()  # TODO kiedy cli bedzie gotowy sprawdzic gdzie to
        #   sie zapisuje, czy w folderze cli czy aktualnym
        #    folderze
    spinner.stop()
    print("Downloading finished!")


def download_full_playlist(url: str, target: Optional[str]) -> None:
    yt_playlist = try_except_playlist(url)

    spinner = Halo(text=f'Downloading: {Playlist(url).title}', spinner='dots')
    spinner.start()

    if yt_playlist is None:
        print("No videos were found")
        exit(7)
    elif target:
        [video.streams.get_highest_resolution().download(target) for video in
         yt_playlist]
    else:
        # TODO stwórz folder na podstawie nazwy tytułu plislity + kanału channel_name
        [video.streams.get_highest_resolution().download() for video in
         yt_playlist]

    spinner.stop()

    print("Downloading finished!")


def playlist_title_url(url: str) -> list:
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
        # TODO czemu nie działa z from rich import print?
        # hyperlink = f"[link={link}]{video_title}[/link]"
        video_title_link = f"{video_title}: {link}. Availability: " \
                           f"{video_ck_aval}"
        titles_links.append(video_title_link)

    spinner.stop()

    return titles_links
