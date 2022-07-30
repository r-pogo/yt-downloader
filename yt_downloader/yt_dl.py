# Third-party imports
from pytube import YouTube, Playlist, exceptions
from halo import Halo


# TODO funkcje do wyszukiwania filmikow tak jak to robie w prawidziwym YT
# TODO funkcja do sciagania filmikow na podstawie kanalu
# TODO funkcja do wyszukiwania filmikow w danym knalae
# TODO funkcja ktora bedzie tworzyc folder na podstawie nazwy kanalu i tam
#  bedzie zapisywac filmiki
def _try_except_youtube(url: str) -> YouTube:
    try:
        youtube = YouTube(url)
    except exceptions.VideoUnavailable:
        print(f'Video {youtube.title} is unavailable.')
        exit(1)

    return youtube


def _try_except_playlist(url: str) -> list[YouTube]:
    playlist_to_check = Playlist(url)

    playlist_to_return = []
    for url in playlist_to_check.video_urls:
        try:
            youtube = YouTube(url)
            playlist_to_return.append(youtube)
        except exceptions.VideoUnavailable:
            print(f'Video {youtube.title} is unavailable, skipping.')
            continue

    return playlist_to_return


def download_single_video(url: str, target: str) -> None:
    # TODO jesli dam path w stylu windowsowskim do linuxa to taget bedzie
    #  None, zrobic cos co przetwarza target na uniwersalny
    spinner = Halo(text=f'Downloading: {YouTube(url).title}', spinner='dots')
    spinner.start()

    youtube = _try_except_youtube(url)
    video = youtube.streams.get_highest_resolution()

    if target:
        video.download(target)
    else:
        video.download()  # TODO kiedy cli bedzie gotowy sprawdzic gdzi to
        #   sie zapisuje, czy w folderze cli czy aktualnym
        #    folderze
    spinner.stop()

    print("Downloading finished!")


def download_full_playlist(url: str, target: str) -> None:
    spinner = Halo(text=f'Downloading: {Playlist(url).title}', spinner='dots')
    spinner.start()

    playlist = _try_except_playlist(url)

    if playlist is None:
        print("All videos are unavailable")
        exit(2)
    elif target:
        [video.streams.get_highest_resolution().download(target) for video in
         playlist]
    else:
        [video.streams.get_highest_resolution().download() for video in
         playlist]

    spinner.stop()

    print("Downloading finished!")


def playlist_title_url(url: str) -> list:
    spinner = Halo(text=f'Downloading titles and links for '
                        f'{Playlist(url).title}', spinner='dots')
    spinner.start()

    video_links = Playlist(url).video_urls

    titles_links = []
    for link in video_links:
        video_title = YouTube(link).title
        video_ck_aval = YouTube(link).check_availability()
        if video_ck_aval is None:
            video_ck_aval = "ok"
        video_title_link = f"{video_title}: {link}. Availability: " \
                           f"{video_ck_aval}"
        titles_links.append(video_title_link)

    spinner.stop()

    return titles_links
