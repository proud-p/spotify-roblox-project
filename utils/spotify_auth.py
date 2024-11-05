# run once to get cache for oauth

import configparser
import spotipy
from spotipy.oauth2 import SpotifyOAuth
import os


# Read Spotify credentials from a configuration file
config = configparser.ConfigParser()
config.read('auth/spotify_keys.ini')

client_id = config['SpotifyAPI']['client_id']
client_secret = config['SpotifyAPI']['client_secret']
username = config['SpotifyAPI']['username']
redirectURI = config['SpotifyAPI']['redirect']

scope = "user-read-private user-read-playback-state user-modify-playback-state playlist-modify-public playlist-modify-private ugc-image-upload"

# Create a SpotifyOAuth object for automated token management
sp_oauth = SpotifyOAuth(client_id=client_id, 
                        client_secret=client_secret, 
                        redirect_uri=redirectURI, 
                        scope=scope, 
                        username=username)

# Get the token programmatically
token_info = sp_oauth.get_cached_token()
if not token_info:
    auth_url = sp_oauth.get_authorize_url()
    print("Please navigate to this URL to authorize:", auth_url)
    response = input("Enter the URL you were redirected to: ")
    code = sp_oauth.parse_response_code(response)
    token_info = sp_oauth.get_access_token(code)
    
token = token_info['access_token']

# Create a Spotify object using the token
sp = spotipy.Spotify(auth=token)

