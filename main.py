import requests
from bs4 import BeautifulSoup
import spotipy
from spotipy.oauth2 import SpotifyOAuth
import os
import pprint

URL = "https://www.billboard.com/charts/hot-100/"

spotify_client_secret = os.environ['SPOTIFY_CLIENT_SECRET']
spotify_client_id = os.environ['SPOTIFY_CLIENT_ID']

date = input('Wich year do you want to travel to? Type the date in this format YYYY-MM-DD: ')

response = requests.get(f"{URL}{date}")
html_doc = response.text

soup = BeautifulSoup(html_doc, 'html.parser')
div_list = soup.select('.chart-element__information__song')
title_list = [tag.string for tag in div_list]
print(title_list)

scope = 'playlist-modify-private'
sp = spotipy.Spotify(auth_manager=SpotifyOAuth(
    scope=scope, client_id=spotify_client_id,
    client_secret=spotify_client_secret,
    redirect_uri='http://example.com',
    show_dialog=True,
    cache_path='token.txt'))

user_id = sp.current_user()['id']

musique = sp.search(q='track:My type', limit=1, type='track')
pp = pprint.PrettyPrinter()
pp.pprint(musique['tracks']['items'][0]['uri'])

song_uri_list = []

# Recupere tous les song URI de notre top 100 musique
for music_title in title_list:
    q = f'track:{music_title}'
    musique = sp.search(q=q, limit=1, type='track')
    try:
        uri = musique['tracks']['items'][0]['uri']
        song_uri_list.append(uri)
    except IndexError:
        print(f"{music_title} n'existe pas sur Spotify.")

# Creer une playlist
playlist_id = sp.user_playlist_create(user=user_id, name=f'{date} Billboard 100', public=False)['id']
# Ajoutes toutes les tracks dans la playlist
sp.playlist_add_items(playlist_id=playlist_id, items=song_uri_list)
