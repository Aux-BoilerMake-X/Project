# BoilerMake - AUX
import spotipy
import json
from dateutil.utils import today
from spotipy.oauth2 import SpotifyOAuth, SpotifyClientCredentials

CLIENT_ID='c287f4b6bc874c2ab63169028d5aedc1'
CLIENT_SECRET='81f3641081dc4e50bc950346f1c2562a'
SPOTIPY_REDIRECT_URI = 'http://localhost:8080'
SCOPE = "user-modify-playback-state playlist-modify-public"
CACHE = '.spotipyoauthcache'
PORT = 8080

sp = spotipy.Spotify(auth_manager=SpotifyOAuth(CLIENT_ID, CLIENT_SECRET,SPOTIPY_REDIRECT_URI,scope=SCOPE,cache_path=CACHE))
user_id = sp.me()['id']

songQueue = []

class Song:
    def __init__(self, title, artist):
        self.title = title
        self.artist = artist
        self.votes = 0


def searchSong(title):
    results = sp.search(title, type='track', limit=5)
    items = results['tracks']['items']
    for item in items:
        print(item['name'])
        name = item['name']
        uri = item['uri']
    return


def addToQueue(song):
    songQueue.append(song)
    return


def upvote(song):
    song.votes += 1


def downvote(song):
    song.votes -= 1


def createNewParty(name):
    date = today()
    sp.user_playlist_create(user=user_id, name=name, public=True, collaborative=False, description=f"Playlist from {name} party, {date}")

def main():
    print("Welcome to AUX!\n Type 1 to create a new party or 2 to join an existing one:")
    option = eval(input())
    if option == 1:
        partyName = input("Name of your new party: ")
        createNewParty(partyName)
        print(f"{partyName} Created!")
    elif option == 2:
        print() #TODO
    else:
        exit()

    searchSong("Rolling in the deep")

if __name__ == '__main__':
    main()