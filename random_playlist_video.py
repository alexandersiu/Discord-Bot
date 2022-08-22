import random
from pytube import Playlist

#this class will take a youtube playlist as an input and will randomly choose a video from the playlist to output
class RandomPlaylistVideo:
    def __init__(self, playlist):
        self.urls = []
        self.playlist = [playlist]

        self.run()

    def get_playlist(self, playlists):
        for playlist in playlists:
            playlists_urls = Playlist(playlist)

        for url in playlists_urls:
            self.urls.append(url)
    
        return self.urls

    def run(self):
        self.pl_urls = self.get_playlist(self.playlist)
        self.index = random.randrange(len(self.pl_urls))
        self.random_video = self.pl_urls[self.index]
        return self.random_video