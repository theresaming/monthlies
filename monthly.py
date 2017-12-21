import sys
import spotipy, datetime
from datetime import datetime
import spotipy.util as util
from months import Months
import creds

scope = 'user-library-read playlist-modify-public playlist-modify-private'

if __name__ == '__main__':
    if len(sys.argv) > 1:
        username = sys.argv[1]
    else:
        print ("Usage: %s username" % (sys.argv[0],))
        sys.exit()

    token = util.prompt_for_user_token(username,scope,client_id=creds.SPOTIPY_CLIENT_ID,client_secret=creds.SPOTIPY_CLIENT_SECRET,redirect_uri=creds.SPOTIPY_REDIRECT_URI)

    if token:
        sp = spotipy.Spotify(auth=token)
        playlist_set = set()
        playlists = sp.user_playlists(username)
        for playlist in playlists['items']:
            if playlist['owner']['id'] == username:
                playlist_set.add(playlist['name'])
        print (playlist_set)
        results = sp.current_user_saved_tracks(limit=20, offset=0)
        current_month = datetime.now().month #month in integer
        current_year = datetime.now().year #year in integer

        for item in results['items']:
            track = item['track']
            added_at = item['added_at']
            date_string = datetime.strptime(added_at, '%Y-%m-%dT%H:%M:%SZ')
            month_added = date_string.month #month of the song added in integer
            year_added = date_string.year

            if month_added != current_month:
                # create a new playlist for that month if one isn't created
                # TODO: only add playlist if one doesn't exist in list
                new_playlist = user_playlist_create(username, month_added + " " + year_added, public=True, description='Created using Spotify Monthlies')
                # TODO: add the track to the playlists

                # TODO: delete that song from the saved tracks

            print (track['name'] + ' - ' + track['artists'][0]['name'] + ' - ' + str(date_string.month))
        print ("current month: " + str(current_month))
        print (Months(current_month))
    else:
        print ("Can't get token for", username)
