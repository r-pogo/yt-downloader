# Third-party imports
from pytube import YouTube, Playlist
from halo import Halo


# TODO funkcje do wyszukiwania filmikow tak jak to robie w prawidziwym YT
# TODO funkcja do sciagania filmikow na podstawie kanalu
# TODO funkcja do wyszukiwania filmikow w danym knalae
# TODO funkcja ktora bedzie tworzyc folder na podstawie nazwy kanalu i tam
#  bedzie zapisywac filmiki


def download_single_video(url: str, target: str) -> None:
    # TODO dodac try exept gdyby youtube niedzialal
    #  https://pytube.io/en/latest/api.html#module-pytube.exceptions
    #  https://pytube.io/en/latest/user/exceptions.html
    # TODO jesli dam path w stylu windowsowskim do linuxa to taget bedzie
    #  None, zrobic cos co przetwarza target na uniwersalny
    youtube = YouTube(url)
    spinner = Halo(text=f'Downloading: {youtube.title}', spinner='dots')
    spinner.start()
    video = youtube.streams.get_highest_resolution()
    if target:
        video.download(target)

    else:
        video.download()  # TODO kiedy cli bedzie gotowy sprawdzic gdzi to
        #   sie zapisuje, czy w folderze cli czy aktualnym
        #    folderze
    # TODO wiadomosc czy sciaganie udalo sie czy nie
    spinner.stop()


def download_full_playlist(url: str, target: str) -> None:
    # TODO dodac try exept gdyby youtube niedzialal
    playlist = Playlist(url)
    spinner = Halo(text=f'Downloading: {playlist.title}', spinner='dots')
    spinner.start()
    if target:
        [video.streams.get_highest_resolution().download(target) for video in
         playlist.videos]
    else:
        [video.streams.get_highest_resolution().download() for video in
         playlist.videos]
    spinner.stop()  # TODO wiadomosc czy sciaganie udalo sie czy nie


@Halo(text=f'Downloading titles and links', spinner='dots')
def playlist_title_url(url: str) -> list:
    # TODO zrobic zewnetrzna funkcje ktora zwraca objekt Playlist ale jest w
    #  try i except
    video_links = Playlist(url).video_urls

    titles_links = []
    for link in video_links:
        video_title = YouTube(link).title
        video_title_link = f"{video_title}: {link}"
        titles_links.append(video_title_link)
    return titles_links
