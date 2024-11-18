import requests
import time
from dotenv import load_dotenv
import os

# Load API key from .env file
load_dotenv()
API_KEY = os.getenv('API_KEY')
API_URL = 'https://api.spoonacular.com/recipes/complexSearch'


def fetch_top_recipes():
    # Fetch top 10 recipes
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

            recipes = "\n".join([f"{i+1}. {recipe['title']} - {recipe.get(
                'sourceUrl', 'No URL available')}" for i, recipe in enumerate(data)])
            return recipes
        else:
            return f"Error: {response.status_code} - {response.json().get('message', 'Unknown error')}"
    except Exception as e:
        return f"Exception occurred: {str(e)}"


def process_request():
    while True:
        try:
            with open('request.txt', 'r') as file:
                request = file.read().strip()
                if request.lower() == "get top recipes":
                    print("Processing request...")

                    recipes = fetch_top_recipes()

                    # Write response to 'response.txt'
                    with open('response.txt', 'w') as response_file:
                        response_file.write(recipes)
                    print("Response written to 'response.txt'")
        except FileNotFoundError:
            print("Request file not found. Waiting for request...")
        except Exception as e:
            print(f"Error: {e}")

        time.sleep(2)


if __name__ == "__main__":
    print("Starting Recipe Recommendation Microservice...")
    process_request()
