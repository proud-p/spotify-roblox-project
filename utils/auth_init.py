import os

def auth_init():
    # Define the path to the ini file
    file_path = 'auth/spotify_keys.ini'

    # Check if the file exists
    if not os.path.exists(file_path):
        # Create the directory if it doesn't exist
        os.makedirs(os.path.dirname(file_path), exist_ok=True)
        
        # Create the ini file with the required format
        with open(file_path, 'w') as file:
            file.write("[SpotifyAPI]\n")
            file.write("username = \n")
            file.write("client_id = \n")
            file.write("client_secret = \n")
            file.write("redirect = \n")
        
        print(f"{file_path} has been created with the required format.")
    else:
        print(f"{file_path} already exists.")


    # Make roblox file---
    # Define the path to the Roblox keys ini file
    roblox_file_path = 'auth/roblox_keys.ini'

    # Check if the file exists
    if not os.path.exists(roblox_file_path):
        # Create the directory if it doesn't exist
        os.makedirs(os.path.dirname(roblox_file_path), exist_ok=True)
        
        # Create the ini file with the required format for the RobloxAPI section
        with open(roblox_file_path, 'w') as file:
            file.write("[RobloxAPI]\n")
            file.write("api_key = \n")
            file.write("place_id = \n")
            file.write("client_id = \n")
            file.write("client_secret = \n")
            file.write("redirect_uri = \n")
            file.write("cookie = \n")
        
        print(f"{roblox_file_path} has been created with the required format.")
    else:
        print(f"{roblox_file_path} already exists.")
