import requests
from django.conf import settings

API_URL = "https://api-inference.huggingface.co/models/distilgpt2"
headers = {"Authorization": f"Bearer {settings.HUGGINGFACE_API_KEY}"}

def generate_text(prompt, max_length=100):
    payload = {
        "inputs": prompt,
        "parameters": {"max_length": max_length, "temperature": 0.7}
    }
    response = requests.post(API_URL, headers=headers, json=payload)
    if response.status_code == 200:
        return response.json()[0]["generated_text"]
    return "Erreur lors de la génération."

def generate_game(genre, mood, keywords):
    # Univers
    universe_prompt = f"Un univers de jeu {genre} avec une ambiance {mood} et les thèmes {keywords}."
    universe = generate_text(universe_prompt, 50)

    # Histoire (3 actes simplifiés)
    story_prompt = f"Une histoire en 3 actes pour un jeu {genre} ({mood}) avec {keywords}."
    story = generate_text(story_prompt, 150)

    # Personnages (2 personnages simples)
    char_prompt = f"Deux personnages pour un jeu {genre} ({mood}): nom, rôle, motivation."
    characters = generate_text(char_prompt, 100)

    # Lieux
    location_prompt = f"Un lieu emblématique pour un jeu {genre} ({mood}) avec {keywords}."
    locations = generate_text(location_prompt, 50)

    return {
        "universe": universe,
        "story": story,
        "characters": characters,
        "locations": locations
    }