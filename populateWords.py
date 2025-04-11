import os
import django
from django.conf import settings

# Configuration de l'environnement Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'gameGenerator.settings')
django.setup()

from generator.models import Word

def populate_words():
    # Liste de mots en anglais
    words = {
        'genre': [
            'adventure', 'puzzle', 'action', 'cute', 'fantasy', 'horror', 'sci-fi', 'platformer',
            'strategy', 'racing', 'shooter', 'simulation'
        ],
        'mood': [
            'happy', 'dark', 'mysterious', 'funny', 'calm', 'epic', 'dreamy', 'tense',
            'sad', 'exciting', 'relaxing', 'chaotic'
        ],
        'keyword': [
            'cat', 'forest', 'castle', 'robot', 'star', 'cloud', 'dragon', 'pizza', 'ghost',
            'flower', 'moon', 'river', 'knight', 'magic', 'space', 'sword', 'alien', 'treasure',
            'pirate', 'city', 'mountain', 'ocean'
        ]
    }

    Word.objects.all().delete()
    print("Anciennes données supprimées.")

    for category, word_list in words.items():
        for word in word_list:
            Word.objects.get_or_create(category=category, word=word)
        print(f"Ajouté {len(word_list)} mots pour la catégorie '{category}'.")

if __name__ == "__main__":
    populate_words()