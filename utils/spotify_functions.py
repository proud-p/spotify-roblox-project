# Spotify scopes (INCLUDE ugc-image-upload)
import configparser

config = configparser.ConfigParser()
config.read('auth/spotify_keys.ini')

client_id = config['SpotifyAPI']['client_id']
client_secret = config['SpotifyAPI']['client_secret']
username = config['SpotifyAPI']['username']
redirectURI = config['SpotifyAPI']['redirect']

scope = "user-read-private user-read-playback-state user-modify-playback-state playlist-modify-public playlist-modify-private ugc-image-upload"
token = util.prompt_for_user_token(username, scope, client_id=client_id, client_secret=client_secret, redirect_uri=redirectURI)

sp = spotipy.Spotify(auth=token)