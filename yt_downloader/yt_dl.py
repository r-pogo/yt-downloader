# Third-party imports
from pytube import YouTube, Playlist
from yaspin import yaspin


# TODO funkcje do wyszukiwania filmikow tak jak to robie w prawidziwym YT
# TODO funkcja do sciagania filmikow na podstawie kanalu
# TODO funkcja do wyszukiwania filmikow w danym knalae
# TODO funkcja ktora bedzie tworzyc folder na podstawie nazwy kanalu i tam
#  bedzie zapisywac filmiki


@yaspin(text="Downloading...")  # TODO stworzyc wlany dekorator
#   spinner/progress bar
def download_single_video(url: str, target: str) -> None:
    # TODO dodac try exept gdyby youtube niedzialal
    #  https://pytube.io/en/latest/api.html#module-pytube.exceptions
    #  https://pytube.io/en/latest/user/exceptions.html
    youtube = YouTube(url)
    video = youtube.streams.get_highest_resolution()
    if target:
        video.download(target)

    else:
        video.download()  # TODO kiedy cli bedzie gotowy sprawdzic gdzi to
        #   sie zapisuje, czy w folderze cli czy aktualnym
        #    folderze


@yaspin(text="Downloading...")  # TODO zrobic wlasny decorator spinner/progress
def download_full_playlist(url: str, target: str) -> None:
    # TODO dodac try exept gdyby youtube niedzialal
    playlist = Playlist(url)
    if target:
        [video.streams.get_highest_resolution().download(target) for video in
         playlist.videos]
    else:
        [video.streams.get_highest_resolution().download() for video in
         playlist.videos]


def playlist_title_url(url):
    video_links = Playlist(url).video_urls
    for link in video_links:
        video_title = YouTube(link).title
        print(f"{video_title}: {link}")
