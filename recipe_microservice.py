import requests
import time
from dotenv import load_dotenv
import os

# Load API key from .env file
load_dotenv()
API_KEY = os.getenv('API_KEY')
API_URL = 'https://api.spoonacular.com/recipes/complexSearch'

# Keep track of the last processed request
last_processed_request = None


def fetch_top_recipes():
    """Fetch top 10 recipes from Spoonacular API."""
    params = {
        'apiKey': API_KEY,
        'number': 10,
        'sort': 'popularity',
        'addRecipeInformation': True
    }

    try:
        response = requests.get(API_URL, params=params)
        if response.status_code == 200:
            data = response.json().get('results', [])
            if not data:
                return "No recipes found."

            recipes = "\n".join([f"{i+1}. {recipe.get('title', 'No Title')} - {recipe.get('sourceUrl', 'No URL available')}"
                                 for i, recipe in enumerate(data)])
            return recipes
        elif response.status_code == 429:
            return "Error: Rate limit exceeded. Please try again later."
        else:
            return f"Error: {response.status_code} - {response.json().get('message', 'Unknown error')}"
    except Exception as e:
        return f"Exception occurred: {str(e)}"


def process_request():
    """Continuously process requests from 'request.txt'."""
    global last_processed_request

    while True:
        try:
            # Read the request file
            with open('request.txt', 'r') as file:
                request = file.read().strip()

                # Ignore redundant requests
                if request.lower() == "get top recipes" and request != last_processed_request:
                    print("Processing request...")
                    last_processed_request = request

                    # Fetch recipes and write the response
                    recipes = fetch_top_recipes()
                    with open('response.txt', 'w') as response_file:
                        response_file.write(recipes)
                    print("Response written to 'response.txt'")

                elif not request:
                    print("Request file is empty. Waiting for a valid request...")
        except FileNotFoundError:
            print("Request file not found. Waiting for request...")
        except Exception as e:
            print(f"Error: {e}")

        # Sleep before polling again
        time.sleep(2)


if __name__ == "__main__":
    print("Starting Recipe Recommendation Microservice...")
    process_request()
