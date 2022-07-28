# Third-party imports
from pytube import YouTube, Playlist
from yaspin import yaspin

# TODO jak sciagac na podstawie tytulu?





#print("Title: ", yt.title)

#print("View: ", yt.views)

@yaspin(text="Downloading...") #TODO na windowsie chujowo wyglada, jak zrobic zeby tu byl napis Downloadng: titlite
def download_single_video(url: str, target: str) -> None:
    # TODO dodac try exept gdyby you tube niedzialal https://pytube.io/en/latest/api.html#module-pytube.exceptions https://pytube.io/en/latest/user/exceptions.html
    youtube = YouTube(url)
    video = youtube.streams.get_highest_resolution()
    if target:
        video.download(target)

    else:
        video.download() #TODO kiedy cli bedzie gotowy sprawdzic gdzi to sie zapisuje, czy w folderze cli czy aktualnym folderze



@yaspin(text="Downloading...") # TODO zrobic wlasny decorator  spinner/progress bar
def download_full_playlist(url: str, target: str) -> None: # TODO albo na podstawie tytulu
    playlist = Playlist(url)
    if target:
        [video.streams.get_highest_resolution().download(target) for video in
         playlist.videos]
    else:
        [video.streams.get_highest_resolution().download() for video in
         playlist.videos]


def playlist_title_url(url): # TODO albo na podstawie tytulu jesli sie da
    video_links = Playlist(url).video_urls
    for link in video_links:
        video_title = YouTube(link).title
        print(f"{video_title}: {link}")




