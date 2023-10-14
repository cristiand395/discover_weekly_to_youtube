# Summary
This project includes these features:
- From your Discover Weekly playlist on Spotify, songs will be added to a playlist on your Spotify account.
- From your Discover Weekly playlist on Spotify, songs will be added to a playlist on your YouTube account.(WIP)
  - Seems like Youtube needs domain with ssl certificate to redirect to, so I'm trying to find a workaround.
- Train Spotify algorithm to improve your Discover Weekly playlist with liked songs from YouTube. (WIP) 
- Automate previous features to run every week. (WIP)

# Pre-requisites
- Python 3.6 or higher [Download](https://www.python.org/downloads/)
- pip [Documentation](https://pip.pypa.io/en/stable/installation/)
- Spotify account
- YouTube account

# Usage
- Login to Spotify and save Discover Weekly playlist to your library
- Go to Spotify Developer Dashboard and create a new app [Dashboard](https://developer.spotify.com/dashboard/applications)
  - Name what ever you want
  - Set Redirect URI to `http://127.0.0.1:8080/redirect`
  - Save it
  - Open new app and save Client ID and Client Secret
- Clone this repository
- Install requirements
```
pip install requirements.txt
```
- Create a file named `.env` in the root of the project and add the following:
```
SPOTIFY_CLIENT_ID=<your_client_id>
SPOTIFY_CLIENT_SECRET=<your_client_secret>
```
- Run the script
```
python3 spotifyWeekly.py
```
- (First time) Open `http://127.0.0.1:8080/` and access with your Spotify account
- Ensure the new playlist `Saved Weekly` is created on your Spotify account with the songs from Discover Weekly playlist
- Enjoy!

## Connect to YouTube (WIP)
- Create a project in Youtube Console [Console](https://console.developers.google.com/)
  - Name what ever you want
  - Enable YouTube Data API v3
  - Complete Consent Screen
  - Create credentials
  - Create OAuth client ID
  - Download credentials
  - Rename credentials to `client_secret.json` and move it to the root of the project

# Remember
- After first usage, add to your profile the new playlist (`Saved Weekly`) to not duplicate playlist the next time.

