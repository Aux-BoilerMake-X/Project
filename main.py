# BoilerMake - AUX
import spotipy
import random
import os
import json
import time
from dateutil.utils import today
from spotipy.oauth2 import SpotifyOAuth

CLIENT_ID = 'c287f4b6bc874c2ab63169028d5aedc1'
CLIENT_SECRET = '81f3641081dc4e50bc950346f1c2562a'
SPOTIPY_REDIRECT_URI = 'http://localhost:8080'
SCOPE = "user-modify-playback-state playlist-modify-public user-read-currently-playing"
CACHE = '.spotipyoauthcache'
PORT = 8080

sp = spotipy.Spotify(
    auth_manager=SpotifyOAuth(CLIENT_ID, CLIENT_SECRET, SPOTIPY_REDIRECT_URI, scope=SCOPE, cache_path=CACHE))
user_id = sp.me()['id']

songList = []
Timer = 0


class Song:
    def __init__(self, uri, title, artist, duration, cover):
        self.URI = uri
        self.title = title
        self.artist = artist
        self.duration = duration
        self.cover = cover
        self.votes = 0


def songToJSON(song):
    result = {'uri': song.URI, 'title': song.title, 'artist': song.artist, 'duration': song.duration,
              'album_cover': song.cover}
    jsonResult = json.dumps(result)
    jsonResult = json.loads(jsonResult)
    return jsonResult


def JSONtoSong(songJson):
    song = Song(songJson['uri'], songJson['title'], songJson['artist'], songJson['duration'], songJson['album_cover'])
    return song


def startTimer():
    global Timer
    Timer = 30
    return


def searchSong(title):
    items = sp.search(title, type='track', limit=5)['tracks']['items']
    results = []
    for item in items:
        result = {'uri': item['uri'], 'title': item['name'], 'artist': item['artists'][0]['name'],
                  'duration': float(item['duration_ms']) / 1000,
                  'album_cover': item['album']['images'][0]['url']}
        results.append(result)
    jsonResults = json.dumps(results, indent=2)
    return jsonResults


def addToList(songJson):
    song = Song(songJson['uri'], songJson['title'], songJson['artist'], songJson['duration'], songJson['album_cover'])
    if len(songList) == 0 and (sp.currently_playing() is None or sp.currently_playing()['is_playing'] is False):
        try:
            sp.start_playback(uris=[song.URI])
            time.sleep(0.1)
            return
        except:
            print("Alert! Device is Inactive. Please resume playback from your spotify app")
            return
    if len(songList) == 0:
        startTimer()
    for s in songList:
        if s.URI == song.URI:
            print("Alert! This song is already in the list.")
            return
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
    date = today().date()
    playlist = sp.user_playlist_create(user=user_id, name=name, public=True, collaborative=False,
                                       description=f"Playlist from {name} party, {date}")['id']
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


def login(auth):
    global sp, user_id
    sp = spotipy.Spotify(auth=auth)
    user_id = sp.me()['id']


def main():
    print("Welcome to AUX!\n Type 1 to create a new party or 2 to join an existing one: ")
    option = eval(input())
    if option == 1:
        # Get auth_token
        login('BQCFYenWLpENPerFoNQVDHYCJk1nxvY6UHR0K2kMyTKszWs44pkCvv6Vugqg5JJMM7DijDAwpNSIuCfPrndstIMbf9u-vL5ZIOGZyqZrJAHKTOGAjI1FUvC91q302LpaUKO6qOiibSa2HKkDgrOOmmefopnhR9bBsTaMuwkTZIhYb0iyIaLuO4q7czMYCqy6WbD8hzdQXF8xwgYkUVFlnscskcvZ0X2uPZ5eshdUoQ')
        partyName = input("Name of your new party: ")
        playlist = createNewParty(partyName)
        print(f"{partyName} Created!")
    elif option == 2:
        print()  # TODO
    else:
        exit()

    # Assume now in common room
    # Search happens here
    print()
    results = json.loads(searchSong("Rauw Alejandro"))
    for r in results:
        addToList(r)

    global Timer

    while True:
        while Timer:
            mins, secs = divmod(Timer, 60)
            timer = '{:02d}:{:02d}'.format(mins, secs)
            print(timer, end="\r")

            if Timer % 5 == 0:
                number = random.randint(0, len(songList) - 1)
                choice = random.randint(0, 1)
                if choice == 0:
                    upvote(songList[number])
                else:
                    downvote(songList[number])

            time.sleep(1)
            Timer -= 1

        # Remove top song and add to queue
        if len(songList) != 0:
            try:
                sp.add_to_queue(uri=songList[0].URI)
                sp.playlist_add_items(playlist, [songList[0].URI])
                songList.pop(0)
            except:
                print("Alert! Device is Inactive. Please resume playback from your spotify app")

        if len(songList) != 0:
            Timer = 30


main()
