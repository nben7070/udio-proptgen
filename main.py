from spotify_client import SpotifyClient
from prompt_generator import PromptGenerator

def main(url):
    # Replace with your Spotify API credentials
    client_id = '{YOUR_CLIENT_ID}'
    client_secret = '{YOUR_CLIENT_SECRET}'

    assert "CLIENT_ID" not in client_id and "CLIENT_SECRET" not in client_secret, "replace dummy values with actual id and key"

    # Create an instance of the SpotifyClient
    spotify_client = SpotifyClient(client_id, client_secret)

    # Replace with the IDs of the playlists you want to analyze
    # playlist_ids = spotify_client.get_playlists_in_folder("PromptGen")
    # print("Playlists fetched")

    playlist_ids = [url[:-1].split("/")[-1].split("?")[0]
]
    playlists = []
    for playlist_id in playlist_ids:
        # Retrieve playlist tracks
        playlist_tracks = spotify_client.get_playlist_tracks(playlist_id)

        playlist_data = []
        print(f"Analyzing {len(playlist_tracks)} tracks")
        for track in playlist_tracks:
            track_id = track['track']['id']
            track_data = spotify_client.get_track_data(track_id)
            if track_data:
                playlist_data.append(track_data)

        playlists.append(playlist_data)
        if len(playlists) % 10 == 0:
            print(f"Playlist length at {len(playlists)}")

    # Create an instance of the PromptGenerator
    prompt_generator = PromptGenerator()
    print("Generating prompts")

    # Generate prompts with different numbers of genres
    for _ in range(2):
        for num_genres in range(1, 4):
            prompt = prompt_generator.generate_prompt(playlists, genres=num_genres)
            print(f"Prompt with {num_genres} genre(s):")
            print(prompt)
            print()


if __name__ == '__main__':
    url = input("Enter spotify playlist url: ")
    while 'spotify.com/playlist' not in url:
        url = input("Ensure url contains spotify.com/playlist: ")
    main(url)
