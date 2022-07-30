# Third-party imports
from pytube import YouTube, Playlist
from halo import Halo


# TODO funkcje do wyszukiwania filmikow tak jak to robie w prawidziwym YT
# TODO funkcja do sciagania calego kanalu
# TODO funkcja ktora bedzie tworzyc folder na podstawie nazwy kanalu i tam
#  bedzie zapisywac filmiki

def download_single_video(you_tube: YouTube, target: str) -> None:
    # TODO jesli dam path w stylu windowsowskim do linuxa to taget bedzie
    #  None, zrobic cos co przetwarza target na uniwersalny
    spinner = Halo(text=f'Downloading: {you_tube.title}', spinner='dots')
    spinner.start()

    video = you_tube.streams.get_highest_resolution()

    if target:
        video.download(target)
    else:
        video.download()  # TODO kiedy cli bedzie gotowy sprawdzic gdzi to
        #   sie zapisuje, czy w folderze cli czy aktualnym
        #    folderze
    spinner.stop()

    print("Downloading finished!")


def download_full_playlist(yt_playlist: list[YouTube], target: str, url: str) -> None:
    spinner = Halo(text=f'Downloading: {Playlist(url).title}', spinner='dots')
    spinner.start()

    if yt_playlist is None:
        print("All videos are unavailable")
        exit(6)
    elif target:
        [video.streams.get_highest_resolution().download(target) for video in
         yt_playlist]
    else:
        [video.streams.get_highest_resolution().download() for video in
         yt_playlist]

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
