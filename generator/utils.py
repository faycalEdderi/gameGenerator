import requests
from django.conf import settings
from huggingface_hub import InferenceClient
from django.core.files.base import ContentFile
from io import BytesIO


HUGGINGFACE_API_URL = settings.HUGGINGFACE_API_URL
headers = {"Authorization": f"Bearer {settings.HUGGINGFACE_API_KEY}"}

def generate_text(prompt, max_length=100):
    payload = {
        "inputs": prompt,
        "parameters": {
            "max_length": max_length,
            "temperature": 0.7,
            "top_k": 50,
            "do_sample": True,
            "return_full_text": False  # Ne renvoie pas le prompt dans le résultat
        }
    }
    try:
        response = requests.post(HUGGINGFACE_API_URL, headers=headers, json=payload)
        if response.status_code == 200:
            result = response.json()
            if isinstance(result, list) and "generated_text" in result[0]:
                generated_text = result[0]["generated_text"].strip()
                return generated_text if generated_text else "No text generated"
            else:
                print(f"Unexpected response: {result}")
                return "Text generation failed"
        else:
            print(f"API error: {response.status_code} - {response.text}")
            return "API request failed"
    except Exception as e:
        print(f"Error: {e}")
        return "Text generation error"

def generate_game(genre, mood, keywords):
    universe_prompt = f"Describe a {genre} game universe with a {mood} vibe, featuring retro graphics and absurd situations tied to '{keywords}'."
    universe = generate_text(universe_prompt, 50)

    story_prompt = f"Tell a 3-act story for a {genre} {mood} game: Act 1 - introduce a quirky hero, Act 2 - present a hilarious problem, Act 3 - resolve it unexpectedly, using '{keywords}'."
    story = generate_text(story_prompt, 150)

    char_prompt = f"Create two characters for a {genre} {mood} game: give their names, comic roles (e.g., clumsy hero, silly villain), and absurd motivations, linked to '{keywords}'."
    characters = generate_text(char_prompt, 100)

    location_prompt = f"Describe an iconic {mood} location for a {genre} game, with retro visuals and a connection to '{keywords}'."
    locations = generate_text(location_prompt, 50)

    return {
        "universe": universe,
        "story": story,
        "characters": characters,
        "locations": locations
    }


def generate_image(prompt):
    client = InferenceClient(
        provider="fal-ai",
        api_key=settings.HUGGINGFACE_API_KEY
    )
    image = client.text_to_image(
        prompt,
        model="black-forest-labs/FLUX.1-dev"
    )
    buffer = BytesIO()
    image.save(buffer, format='PNG')
    image_file = ContentFile(buffer.getvalue(), name="game_image.png")
    return image_file