import random

class PromptGenerator:
    """
    A class for generating prompts based on track data from multiple playlists.

    The PromptGenerator class takes a list of playlists containing track data, and generates a prompt
    that describes a hypothetical track based on the characteristics of the tracks in the playlists.

    The class performs the following steps:
    1. Initializes mapping dictionaries to map audio feature values to descriptive terms.
    2. Receives a list of playlists containing track data.
    3. Calculates the distribution of audio feature values and genres across all tracks in the playlists.
    4. Randomly chooses values for energy, valence, danceability, and tempo based on their distribution.
    5. Randomly selects a primary genre and additional influencing genres based on the genre distribution
       and the specified number of genres.
    6. Generates a prompt string that includes the selected genre(s) and descriptive terms for energy,
       valence, danceability, and tempo.
    7. Returns the generated prompt.

    Example usage:
        prompt_generator = PromptGenerator()
        playlists = [
            [
                {
                    'track_info': {},
                    'audio_features': {
                        'energy': 0.8,
                        'valence': 0.6,
                        'danceability': 0.7,
                        'tempo': 120
                    },
                    'genres': ['pop', 'electronic']
                },
                ...
            ],
            ...
        ]
        prompt = prompt_generator.generate_prompt(playlists, genres=3)
        print(prompt)
        # Output: "Generate a pop track with electronic and rock influence, high energy,
        #          happy mood, high danceability, and fast tempo."
    """

    def __init__(self):
        self.energy_map = {
            (0.0, 0.3): 'low',
            (0.3, 0.7): 'medium',
            (0.7, 1.0): 'high'
        }
        self.valence_map = {
            (0.0, 0.3): 'sad',
            (0.3, 0.7): 'neutral',
            (0.7, 1.0): 'happy'
        }
        self.danceability_map = {
            (0.0, 0.3): 'low',
            (0.3, 0.7): 'medium',
            (0.7, 1.0): 'high'
        }
        self.tempo_map = {
            (0, 80): 'slow',
            (80, 120): 'medium',
            (120, 200): 'fast'
        }
        self.key_map = pitch_class_to_key = {
            '0': 'C',
            '1': 'C#/Db',
            '2': 'D',
            '3': 'D#/Eb',
            '4': 'E',
            '5': 'F',
            '6': 'F#/Gb',
            '7': 'G',
            '8': 'G#/Ab',
            '9': 'A',
            '10': 'A#/Bb',
            '11': 'B'
        }

    def map_feature_to_term(self, feature_value, feature_map):
        """
        Maps a feature value to its corresponding descriptive term based on the provided mapping dictionary.

        Args:
            feature_value (float): The value of the audio feature.
            feature_map (dict): A dictionary mapping feature ranges to descriptive terms.

        Returns:
            str: The descriptive term corresponding to the feature value.
        """

        for range_, term in feature_map.items():
            if range_[0] <= feature_value <= range_[1]:
                return term
        return 'medium'

    def generate_prompt(self, playlists, genres=1):
        """
        Generates a prompt based on the track data from multiple playlists.

        The prompt includes the selected genre(s) and descriptive terms for energy, valence,
        danceability, and tempo, which are randomly chosen based on their distribution across
        all tracks in the playlists.

        Args:
            playlists (list): A list of playlists, where each playlist is a list of track data dictionaries.
                Each track data dictionary should have the following structure:
                {
                    'track_info': {},
                    'audio_features': {
                        'energy': float,
                        'valence': float,
                        'danceability': float,
                        'tempo': float
                    },
                    'genres': list
                }
            genres (int, optional): The number of genres to include in the prompt. Defaults to 1.

        Returns:
            str: The generated prompt as a string.
        """

        all_track_data = [track_data for playlist in playlists for track_data in playlist]

        # Calculate the distribution of audio features and genres
        energy_values = [track_data['audio_features']['energy'] for track_data in all_track_data]
        valence_values = [track_data['audio_features']['valence'] for track_data in all_track_data]
        danceability_values = [track_data['audio_features']['danceability'] for track_data in all_track_data]
        tempo_values = [track_data['audio_features']['tempo'] for track_data in all_track_data]
        key_values = [str(track_data['audio_features']['key']) for track_data in all_track_data]
        genre_counts = {}
        for track_data in all_track_data:
            for genre in track_data['genres']:
                genre_counts[genre] = genre_counts.get(genre, 0) + 1

        # Randomly choose values based on the distribution
        energy_value = random.choices(energy_values, k=1)[0]
        valence_value = random.choices(valence_values, k=1)[0]
        danceability_value = random.choices(danceability_values, k=1)[0]
        tempo_value = random.choices(tempo_values, k=1)[0]
        key_value = random.choices(key_values, k=1)[0]
        genre_list = random.choices(list(genre_counts.keys()), weights=list(genre_counts.values()), k=genres)
        genre_list = list(set(genre_list))

        # Map the chosen values to descriptive terms
        energy_term = self.map_feature_to_term(energy_value, self.energy_map)
        valence_term = self.map_feature_to_term(valence_value, self.valence_map)
        danceability_term = self.map_feature_to_term(danceability_value, self.danceability_map)
        tempo_term = self.map_feature_to_term(tempo_value, self.tempo_map)
        key_term = self.key_map[key_value]


        # Generate the prompt
        prompt = f"A {genre_list[0]} track"
        if genres > 1:
            genre_influences = " and ".join(genre_list[1:])
            prompt += f" with {genre_influences} influence"
        prompt += f", {energy_term} energy, {valence_term} mood, {danceability_term} danceability, and {tempo_term} tempo in a {key_term} key."

        return prompt

