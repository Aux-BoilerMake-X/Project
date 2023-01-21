# BoilerMake - AUX
import spotipy
import os
import json
import time
from dateutil.utils import today
from spotipy.oauth2 import SpotifyOAuth, SpotifyClientCredentials

CLIENT_ID='c287f4b6bc874c2ab63169028d5aedc1'
CLIENT_SECRET='81f3641081dc4e50bc950346f1c2562a'
SPOTIPY_REDIRECT_URI = 'http://localhost:8080'
SCOPE = "user-modify-playback-state playlist-modify-public user-read-currently-playing"
CACHE = '.spotipyoauthcache'
PORT = 8080

#sp = spotipy.Spotify(auth_manager=SpotifyOAuth(CLIENT_ID, CLIENT_SECRET,SPOTIPY_REDIRECT_URI,scope=SCOPE,cache_path=CACHE))
sp = spotipy.Spotify(auth='BQDNckygXpFd0n2GXPZbjQd0PJu_MIpwkuEpMdhticg0tfWl09UsjAaD6juk1LjJnza9PA9h9Ul3e47CwFRNhQ4awPqL32gPtKHz0QGBSp-T5ikFqQUeYLr3-aSMJBWR-nPTwtECiDdEG0yboCgCxLXkbtZC8GfPJ8Zv9w0Ll3fFp0Bhy11MILyESF7S6RXUa25FAsP7-jg6MjbLBg')
user_id = sp.me()['id']

songList = []
global Timer

class Song:
    def __init__(self, uri, title, artist, duration, cover):
        self.URI = uri
        self.title = title
        self.artist = artist
        self.duration = duration
        self.cover = cover
        self.votes = 0

def startTimer():
    Timer = 120
    return

def searchSong(title):
    items = sp.search(title, type='track', limit=10)['tracks']['items']
    results = []
    for item in items:
        result = {'uri': item['uri'], 'title': item['name'], 'artist': item['artists'][0]['name'], 'duration': float(item['duration_ms']) / 1000,
                  'album_cover': item['album']['images'][0]['url']}
        results.append(result)
    jsonResults = json.dumps(results)
    return jsonResults

def addToList(songJson):
    song = Song(songJson['uri'], songJson['title'], songJson['artist'], songJson['duration'], songJson['album_cover'])
    if len(songList) == 0 and not sp.currently_playing():
        sp.start_playback(song.URI)
        return
    startTimer()
    songList.append(song)
    refresh()
    return

def upvote(song):
    song.votes += 1
    sortList()


def downvote(song):
    song.votes -= 1
    sortList()

def createNewParty(name):
    date = today()
    playlist = sp.user_playlist_create(user=user_id, name=name, public=True, collaborative=False, description=f"Playlist from {name} party, {date}")
    return playlist

def sortList():
    songList.sort(key=lambda x: x.votes, reverse=True)
    refresh()


def refresh():
    os.system('cls')
    for song in songList:
        color = '\033[1m'
        if song.votes > 0:
            color = '\033[92m'
        elif song.votes < 0:
            color = '\033[91m'
        endc = '\033[0m'
        print(f"{song.title:<30}{color}{song.votes:>6}{endc}")
    print("\n")
    time.sleep(3)

def main():
    print("Welcome to AUX!\n Type 1 to create a new party or 2 to join an existing one:")
    option = eval(input())
    if option == 1:
        partyName = input("Name of your new party: ")
        playlist = createNewParty(partyName)
        print(f"{partyName} Created!")
    elif option == 2:
        print() #TODO
    else:
        exit()

    # Assume now in common room
    # Search happens here
    print()
    results = json.loads(searchSong("Adele"))
    for r in results:
        addToList(r)
    upvote(songList[0])
    upvote(songList[0])
    upvote(songList[4])
    downvote(songList[7])


if __name__ == '__main__':
    main()