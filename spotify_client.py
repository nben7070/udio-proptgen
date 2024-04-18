import spotipy
from spotipy.oauth2 import SpotifyClientCredentials

class SpotifyClient:
    def __init__(self, client_id, client_secret):
        self.client_id = client_id
        self.client_secret = client_secret
        self.sp = self._authenticate()

    def _authenticate(self):
        client_credentials_manager = SpotifyClientCredentials(
            client_id=self.client_id,
            client_secret=self.client_secret
        )
        return spotipy.Spotify(client_credentials_manager=client_credentials_manager)

    def get_track_info(self, track_id):
        try:
            track_info = self.sp.track(track_id)
            return track_info
        except spotipy.exceptions.SpotifyException as e:
            print(f"Error retrieving track information: {e}")
            return None

    def get_audio_features(self, track_id):
        try:
            audio_features = self.sp.audio_features(track_id)
            return audio_features[0] if audio_features else None
        except spotipy.exceptions.SpotifyException as e:
            print(f"Error retrieving audio features: {e}")
            return None

    def get_artist_genres(self, artist_id):
        try:
            artist_info = self.sp.artist(artist_id)
            return artist_info['genres']
        except spotipy.exceptions.SpotifyException as e:
            print(f"Error retrieving artist genres: {e}")
            return []

    def get_track_data(self, track_id):
        track_info = self.get_track_info(track_id)
        if track_info is None:
            return None

        audio_features = self.get_audio_features(track_id)
        if audio_features is None:
            return None

        artist_id = track_info['artists'][0]['id']
        genres = self.get_artist_genres(artist_id)

        track_data = {
            'track_info': track_info,
            'audio_features': audio_features,
            'genres': genres
        }

        return track_data

    def get_playlist_tracks(self, playlist_id):
        try:
            tracks = []
            results = self.sp.playlist_tracks(playlist_id)
            tracks.extend(results['items'])
            while results['next']:
                results = self.sp.next(results)
                tracks.extend(results['items'])
            return tracks
        except spotipy.exceptions.SpotifyException as e:
            print(f"Error retrieving playlist tracks: {e}")
            return []

    def get_user_playlists(self):
        try:
            playlists = []
            results = self.sp.current_user_playlists()
            playlists.extend(results['items'])
            while results['next']:
                results = self.sp.next(results)
                playlists.extend(results['items'])
            return playlists
        except spotipy.exceptions.SpotifyException as e:
            print(f"Error retrieving user playlists: {e}")
            return []

    def get_playlists_in_folder(self, folder_name):
        """
        Retrieves all playlists in a user's folder by the folder name.

        Args:
            folder_name (str): The name of the folder to retrieve playlists from.

        Returns:
            list: A list of playlists in the specified folder.
        """
        try:
            # Retrieve the list of all folders for the user
            folders = self.sp.current_user_playlists(limit=50)

            # Find the folder with the specified name
            target_folder = None
            while folders:
                for folder in folders['items']:
                    if folder['name'] == folder_name:
                        target_folder = folder
                        break

                if target_folder:
                    break

                if folders['next']:
                    folders = self.sp.next(folders)
                else:
                    break

            if target_folder:
                # Retrieve all playlists in the target folder
                playlists = []
                offset = 0
                while True:
                    folder_playlists = self.sp.user_playlist_tracks(playlist_id=target_folder['id'], limit=100,
                                                                    offset=offset)
                    playlists.extend(folder_playlists['items'])

                    if folder_playlists['next']:
                        offset += len(folder_playlists['items'])
                    else:
                        break

                return playlists
            else:
                print(f"Folder '{folder_name}' not found.")
                return []

        except spotipy.exceptions.SpotifyException as e:
            print(f"Error retrieving playlists in folder: {e}")
            raise e

