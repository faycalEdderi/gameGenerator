from transformers import pipeline

generator = pipeline("text-generation", model="gpt2", device=0)

def generate_text(prompt, max_length=100):
    try:
        result = generator(prompt, max_length=max_length, temperature=0.7, top_k=50, num_return_sequences=1)
        generated_text = result[0]["generated_text"]
        cleaned_text = generated_text.replace(prompt, "").strip()
        return cleaned_text if cleaned_text else generated_text 
    except Exception as e:
        print(f"Erreur : {e}")
        return "Texte non généré"

def generate_game(genre, mood, keywords):
    universe_prompt = f"Décris un univers de jeu {genre} {mood} avec des graphismes rétro et des situations absurdes liées à '{keywords}'."
    universe = generate_text(universe_prompt, 50)

    story_prompt = f"Raconte une histoire en 3 actes pour un jeu {genre} {mood} : Acte 1 - introduction d’un héros loufoque, Acte 2 - un problème hilarant, Acte 3 - une résolution inattendue, avec '{keywords}'."
    story = generate_text(story_prompt, 150)

    char_prompt = f"Invente deux personnages pour un jeu {genre} {mood} : donne leur nom, un rôle comique (ex. héros maladroit, méchant ridicule), et une motivation absurde, liés à '{keywords}'."
    characters = generate_text(char_prompt, 100)

    location_prompt = f"Décris un lieu emblématique et {mood} pour un jeu {genre}, avec des détails visuels rétro et un lien à '{keywords}'."
    locations = generate_text(location_prompt, 50)

    return {
        "universe": universe,
        "story": story,
        "characters": characters,
        "locations": locations
    }