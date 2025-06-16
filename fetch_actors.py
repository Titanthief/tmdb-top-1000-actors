import requests
import csv
import time
import os
from typing import List, Dict, Optional

class TMDBClient:
    def __init__(self, api_key: str):
        self.api_key = api_key
        self.base_url = "https://api.themoviedb.org/3"
        self.headers = {
            "accept": "application/json",
            "Authorization": f"Bearer {api_key}"
        }
    
    def get_popular_actors(self, page: int = 1) -> Dict:
        """Fetch popular actors from TMDb API"""
        url = f"{self.base_url}/person/popular"
        params = {
            "api_key": self.api_key,
            "page": page,
            "language": "en-US"
        }
        
        response = requests.get(url, params=params)
        if response.status_code == 200:
            return response.json()
        else:
            raise Exception(f"API request failed: {response.status_code}")
    
    def get_actor_details(self, actor_id: int) -> Optional[Dict]:
        """Get detailed information about an actor"""
        url = f"{self.base_url}/person/{actor_id}"
        params = {
            "api_key": self.api_key,
            "language": "en-US",
            "append_to_response": "movie_credits"
        }
        
        response = requests.get(url, params=params)
        if response.status_code == 200:
            return response.json()
        else:
            print(f"Failed to get details for actor ID {actor_id}")
            return None
    
    def get_known_for_movies(self, actor_data: Dict) -> str:
        """Extract known for information from actor's movie credits"""
        if 'movie_credits' not in actor_data or 'cast' not in actor_data['movie_credits']:
            return "Actor/Actress"
        
        # Get top movies by popularity
        movies = actor_data['movie_credits']['cast']
        movies.sort(key=lambda x: x.get('popularity', 0), reverse=True)
        
        # Take top 2-3 most popular movies
        top_movies = movies[:3]
        movie_names = [movie['title'] for movie in top_movies if movie.get('title')]
        
        if movie_names:
            if len(movie_names) == 1:
                return f"Known for {movie_names[0]}"
            elif len(movie_names) == 2:
                return f"Known for {movie_names[0]} and {movie_names[1]}"
            else:
                return f"Known for {movie_names[0]}, {movie_names[1]}, and {movie_names[2]}"
        
        return "Actor/Actress"

def fetch_actors_data(api_key: str, target_count: int = 1000) -> List[Dict]:
    """Fetch actor data from TMDb API"""
    client = TMDBClient(api_key)
    actors_data = []
    page = 1
    
    print(f"Fetching {target_count} actors from TMDb API...")
    
    while len(actors_data) < target_count:
        try:
            print(f"Fetching page {page}...")
            response = client.get_popular_actors(page)
            
            if not response.get('results'):
                print("No more results available")
                break
            
            for actor in response['results']:
                if len(actors_data) >= target_count:
                    break
                
                # Get detailed information for each actor
                actor_details = client.get_actor_details(actor['id'])
                if actor_details:
                    # Build photo URL
                    photo_path = actor_details.get('profile_path')
                    if photo_path:
                        photo_url = f"https://image.tmdb.org/t/p/w500{photo_path}"
                    else:
                        photo_url = "No photo available"
                    
                    # Get known for information
                    known_for = client.get_known_for_movies(actor_details)
                    
                    actors_data.append({
                        'name': actor_details.get('name', 'Unknown'),
                        'photo': photo_url,
                        'known_for': known_for
                    })
                    
                    print(f"Added: {actor_details.get('name', 'Unknown')}")
                
                # Rate limiting to be respectful to the API
                time.sleep(0.1)
            
            page += 1
            
        except Exception as e:
            print(f"Error fetching page {page}: {e}")
            break
    
    print(f"Successfully fetched {len(actors_data)} actors")
    return actors_data

def save_to_csv(actors_data: List[Dict], filename: str = "famous_actors.csv"):
    """Save actor data to CSV file"""
    with open(filename, 'w', newline='', encoding='utf-8') as csvfile:
        fieldnames = ['name', 'photo', 'known_for']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        
        writer.writeheader()
        for actor in actors_data:
            writer.writerow(actor)
    
    print(f"CSV file saved as {filename}")

def main():
    # Your TMDb API key
    api_key = "your_api_goes_here"
    
    try:
        # Fetch actor data
        actors_data = fetch_actors_data(api_key, 1000)
        
        # Save to CSV
        save_to_csv(actors_data)
        
        print(f"\nSuccessfully created CSV file with {len(actors_data)} actors!")
        print("The CSV file contains: name, photo URL, and known for information")
        
    except Exception as e:
        print(f"An error occurred: {e}")

if __name__ == "__main__":
    main() 
