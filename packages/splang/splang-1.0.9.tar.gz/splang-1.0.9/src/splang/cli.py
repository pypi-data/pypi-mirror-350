# splang/src/splang/cli.py
import json
import sys
import spotipy
import os
import importlib.resources
from splang.utils import get_last_second, get_first_second, process_ms, get_first_ascii_character
from splang.interpreter import SplangInterpreter

def get_all_playlists(sp):
    playlists = []
    results = sp.current_user_playlists()
    while results:
        playlists.extend(results['items'])
        if results['next']:
            results = sp.next(results)
        else:
            break
    return playlists

def get_all_tracks_from_playlist(sp, playlist_id):
    all_tracks = []
    results = sp.playlist_tracks(playlist_id)
    while results:
        all_tracks.extend(results['items'])
        if results['next']:
            results = sp.next(results)
        else:
            break
    return all_tracks

# Get all saved tracks
def get_all_saved_tracks(sp):
    tracks = []
    results = sp.current_user_saved_tracks()
    while results:
        tracks.extend(results['items'])
        if results['next']:
            results = sp.next(results)
        else:
            break
    return tracks

def main():
    # Check if there is the -h flag
    if len(sys.argv) > 1 and sys.argv[1] == '-h':
        print("Usage: splang [path_to_playlist.json]")
        print("Use: splang -hello to use the hello world example, or splang -fib to use the fibonacci example.")
        print("If you want to use a playlist from Spotify, please set the SPOTIPY_CLIENT_ID, SPOTIPY_CLIENT_SECRET, and SPOTIPY_REDIRECT_URI environment variables.")
        print("If no path is provided, the program will prompt you to log into Spotify and select a playlist.")
        sys.exit(0)


    # If a path is provided, load the playlist from the file
    if len(sys.argv) > 1:
        path = sys.argv[1]
        try:
            if sys.argv[1] == '-hello' or sys.argv[1] == '-fib':
                if sys.argv[1] == '-fib':
                    path = "fibonacci.json"
                else:
                    path = "helloworld.json"
                with importlib.resources.files("splang.examples").joinpath(path).open('r') as f:
                    track_data = json.load(f)
                for i, track in enumerate(track_data):
                    print(f"Track {i}: {track['track_name']} - {track['duration_min']}")
            else:
                with open(path, 'r') as f:
                    track_data = json.load(f)
        except FileNotFoundError:
            print(f"Error: File {path} not found.")
            sys.exit(1)
        except json.JSONDecodeError:
            print(f"Error: File {path} is not a valid JSON file.")
            sys.exit(1)

        if not isinstance(track_data, list):
            print(f"Error: File {path} does not contain a valid playlist format. Expected a list of tracks.")
            sys.exit(1)

        #Process track_id, duration_min, first_letter ; Generate opcode, first_second, last_second
        for i, track in enumerate(track_data):
            if not isinstance(track, dict):
                print(f"Error: Track {i} in the playlist is not a valid dictionary.")
                sys.exit(1)

            # If track_id is not valid, set it to a default value
            if 'track_id' not in track or not isinstance(track['track_id'], str):
                track_data[i]['track_id'] = f'track_{i}'
            
            # If first_letter is not valid, set it to a default value
            if 'first_letter' not in track or not isinstance(track['first_letter'], str) or len(track['first_letter']) != 1:
                track_data[i]['first_letter'] = '¿'

            # If duration_min is not valid, set it to a default value
            if 'duration_min' not in track or not isinstance(track['duration_min'], str):
                track_data[i]['duration_min'] = "0:00"

            duration_min = track['duration_min']
            if not isinstance(duration_min, str) or not (len(duration_min.split(':')) == 2 and
                                                         all(part.isdigit() for part in duration_min.split(':')) and
                                                         0 <= int(duration_min.split(':')[1]) < 60):
                print(f"Error: duration_min must be a string in format 'mm:ss' with valid minutes and seconds in track: {track}")
                sys.exit(1)

            # Calculate opcode, first_second, last_second
            last_second = int(duration_min.split(':')[1]) % 10
            first_second = int(duration_min.split(':')[1]) // 10
            opcode = 10 * first_second + last_second
            track['opcode'] = opcode
            track['first_second'] = first_second
            track['last_second'] = last_second

        
    else:
        #Prompt user to log into Spotify
        #Check if SPOTIPY_CLIENT_ID, SPOTIPY_CLIENT_SECRET, and SPOTIPY_REDIRECT_URI are set
        if 'SPOTIPY_CLIENT_ID' not in os.environ or 'SPOTIPY_CLIENT_SECRET' not in os.environ or 'SPOTIPY_REDIRECT_URI' not in os.environ:
            print("Error: SPOTIPY_CLIENT_ID, SPOTIPY_CLIENT_SECRET, and SPOTIPY_REDIRECT_URI must be set in environment variables.")
            print("Please set them and try again.")
            sys.exit(1)
        scope = "user-library-read playlist-read-private playlist-read-collaborative"
        sp = spotipy.Spotify(auth_manager=spotipy.SpotifyOAuth(os.environ['SPOTIPY_CLIENT_ID'],
                                                            os.environ['SPOTIPY_CLIENT_SECRET'],
                                                            os.environ['SPOTIPY_REDIRECT_URI'],
                                                            scope=scope))
        if not sp:
            print("Error: Could not authenticate with Spotify. Please check your credentials.")
            sys.exit(1)

        # Check if the user is logged in
        if not sp.current_user():
            print("Error: You are not logged in to Spotify. Please log in and try again.")
            sys.exit(1)


        # Check if the user has any playlists

        all_tracks = []
        choices = get_all_playlists(sp)
        if len(choices) != 0:
            playlists = []
            # Prompt the user to type which 1 playlist they want to use
            print("Please select the playlist you want to use:")
            for i, playlist in enumerate(choices):
                print(f"{i}: {playlist['name']}")
                playlists.append(playlist)

            # Prompt the user to select one playlist from the options
            selected_playlist = input("Please select a playlist by number: ").strip().lower()
            if selected_playlist.isdigit() and int(selected_playlist) < len(playlists):
                selected_playlist = int(selected_playlist)
                all_tracks = get_all_tracks_from_playlist(sp, playlists[selected_playlist]['id'])
            else:
                print("Invalid selection. Please try again.")
                sys.exit(1)
        else:
            print("No playlists found. Please create a playlist and try again.")
            sys.exit(1)

        track_data = []
        for item in all_tracks:
            track = item['track']
            track_name = track['name']
            track_id = track['id']
            artist_name = track['artists'][0]['name']
            album_name = track['album']['name']
            release_date = track['album']['release_date']
            try:
                spotify_url = track['external_urls']['spotify']
            except KeyError:
                # Handle the case where the Spotify URL is not available
                spotify_url = None

            try:
                # Handle the case where the track does not have a popularity score
                popularity = track['popularity']
            except KeyError:
                # Set a default value for popularity if not available
                popularity = None
            duration_ms= track['duration_ms']
            duration_min = process_ms(duration_ms)
            first_second = get_first_second(duration_min)
            last_second = get_last_second(duration_min)
            first_letter = get_first_ascii_character(track_name)
            track_data.append({
                'track_name': track_name,
                'track_id': track_id,
                'artist_name': artist_name,
                'album_name': album_name,
                'release_date': release_date,
                'spotify_url': spotify_url,
                'duration_ms': duration_ms,
                'popularity': popularity,
                'duration_min': duration_min,
                'first_letter': first_letter,
                'opcode': 10 * first_second + last_second,
                'first_second': first_second,
                'last_second': last_second
            })
        
        # Ask the user if they want to save the playlist to a JSON file
        save_to_json = input("Do you want to save the playlist to a JSON file? (y/n): ").strip().lower()
        if save_to_json != 'y':
            print("Playlist not saved to JSON file.")
            # Continue without saving
            pass
        else:
            # Save to cwd
            json.dump(track_data, open(os.path.join(os.getcwd(), playlists[selected_playlist]['name'] + '.json'), 'w'), indent=4)
            print("Playlist saved to JSON file.")

    # Run the Splang interpreter
    try:
        interp = SplangInterpreter(track_data)
    except Exception as e:
        print("Error initializing the interpreter:", e, file=sys.stderr)
        sys.exit(1)

    try:
        interp.run()
        print("\n")
    except Exception as e:
        print("Error during execution:", e, file=sys.stderr)
        print("Interpreter state at the time of error:")
        print(interp._state())
        sys.exit(1)


        