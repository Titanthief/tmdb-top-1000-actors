<<<<<<< HEAD
# Famous Actor Anki Deck Generator

This project fetches data for 1000 famous actors from The Movie Database (TMDb) API and generates a CSV file suitable for creating an Anki deck.

## Features

- Fetches 1000 popular actors from TMDb API
- Includes actor name, photo URL, and "known for" information
- Generates a CSV file with three columns: name, photo, known_for
- Rate limiting to respect API limits

## Setup

1. Install the required dependencies:
```bash
pip install -r requirements.txt
```

2. Run the script:
```bash
python fetch_actors.py
```

## Output

The script will generate a `famous_actors.csv` file with the following columns:
- **name**: Actor's full name
- **photo**: URL to the actor's profile photo (TMDb image URL)
- **known_for**: 1-2 sentence description of their most famous movies

## Using with Anki

1. Import the CSV file into Anki
2. Set up the card template to display:
   - Front: Actor's name
   - Back: Actor's photo and "known for" information

## API Key

The script uses the provided TMDb API key. The API key is already configured in the script.

## Notes

- The script includes rate limiting (0.1 second delay between requests) to be respectful to the TMDb API
- Photos are provided as URLs to TMDb's image service
- "Known for" information is generated from the actor's most popular movies 
=======
# tmdb-top-1000-actors
A snapshot dataset and Anki deck of the 1000 most talked-about actors worldwide on June 15, 2025, sourced from The Movie Database (TMDb). Includes actor names, headshots, known-for titles, and brief bios. Intended for educational and personal use.
>>>>>>> e7b9855d2bd619b3d8eb563f96665a28e7fb17ef
