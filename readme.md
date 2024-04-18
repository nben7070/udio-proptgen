# Audio Prompt Generator

Audio Prompt Generator is a Python project that takes a Spotify playlist as input and generates a prompt for Udio, an AI-powered audio generation tool, based on the characteristics of the playlist.

## Features

- Extracts playlist information from a provided Spotify playlist URL
- Analyzes the playlist's characteristics, such as genre, mood, tempo, and key
- Generates a selection of potential prompts

## Prerequisites

Before running the Audio Prompt Generator, ensure that you have the following:

- Python 3.x installed on your system
- A Spotify Developer account and API credentials (Client ID and Client Secret)
- The necessary Python libraries installed (see `requirements.txt`)

## Installation

1. Clone the repository:

`git clone https://github.com/yourusername/audio-promptgen.git`

2. Change into the project directory:

`cd audio-promptgen`

3. Install the required Python libraries:

`pip install -r requirements.txt`

4. Set up your Spotify API credentials:

- Go to the [Spotify Developer Dashboard](https://developer.spotify.com/dashboard/) and create a new application.
- Obtain the Client ID and Client Secret for your application.
- Update the `main.py` file with your Client ID and Client Secret.

## Usage

1. Run the `main.py` script:

`python main.py`

2. When prompted, enter the URL of the Spotify playlist you want to use.

3. The script will analyze the playlist and generate an Udio prompt based on its characteristics.

4. The generated prompts will be displayed in the console.

## Customization

You can customize the prompt generation process by modifying the `PromptGenerator` class in `prompt_generator.py`. This class contains methods for analyzing playlist characteristics and generating the Udio prompt.

Feel free to experiment with different prompt formats, additional playlist characteristics, or integrating other APIs to enhance the prompt generation process.

## Roadmap

A full authorization flow with Spotify will be launched shortly so you'll only need a Spotify account rather than an id and secret. 

A lightweight client will be launched to enable easier interactions and customizations for what values to include

Potentially, I'll do an integration with the udio API to create songs in app

## License

This project is licensed under the [MIT License](LICENSE).

## Acknowledgements

- [Spotify Web API](https://developer.spotify.com/documentation/web-api/)
- [Udio](https://udio.com/)
- [Claude](https://claude.ai)
