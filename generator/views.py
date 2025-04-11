from django.shortcuts import render, redirect

from django.contrib.auth.decorators import login_required
from .forms import GameForm
from .utils import generate_game, generate_image
from .models import Game
from django.utils import timezone
from datetime import timedelta
import os
from django.conf import settings
import random
from django.http import HttpResponse

"""
Handles the creation of a new game for the logged-in user.

This view allows users to create a game by filling out a form. An image is also generated using AI. It enforces a limit
of 5 games per hour per user. If the limit is reached, the user is redirected to a
page informing them of the restriction. Otherwise, the form is displayed, and upon
submission, the game is generated and saved to the database.

Args:
    request (HttpRequest): The HTTP request object containing metadata about the request.

Returns:
    HttpResponse: Renders the game creation form or redirects to the game detail page
                  upon successful creation. If the game limit is reached, renders a
                  limit notification page.
"""
@login_required
def create_game(request):
    time_limit = timezone.now() - timedelta(hours=1)
    recent_games = Game.objects.filter(user=request.user, created_at__gte=time_limit).count()
    if recent_games >= 5:
        return render(request, "generator/limit_reached.html", {
            "limit": 5,
            "period": "heure"
        })

    if request.method == "POST":
        if 'random_fill' in request.POST:
            initial_data = random_game()
            print(initial_data)
            form = GameForm(initial=initial_data)
            return render(request, "generator/create_game.html", {"form": form})
        else:
            form = GameForm(request.POST)
            if form.is_valid():
                data = form.cleaned_data
                game_data = generate_game(data["genre"], data["mood"], data["keywords"])
                
                # Génère l’image basée sur les mots-clés
                image_prompt = f"A {data['genre']} game with {data['mood']} ambiance featuring {data['keywords']}"
                image_file = generate_image(image_prompt)
                game = Game.objects.create(
                    user=request.user,
                    title=f"Jeu {data['genre']} - {data['mood']}",
                    genre=data["genre"],
                    mood=data["mood"],
                    keywords=data["keywords"],
                    story=game_data["story"],
                    characters=game_data["characters"],
                    locations=game_data["locations"],
                    image=image_file
                )
                return redirect("game_detail", game_id=game.id)
    else:
        form = GameForm()
    return render(request, "generator/create_game.html", {"form": form})


"""
Handles the display of a specific game detail page.
This view retrieves the game details from the database and renders them on a page.
It is accessible only to logged-in users. The game detail page displays the
Args:
    request (HttpRequest): The HTTP request object.
Returns:
    HttpResponse: Renders the game creation form, redirects to the game detail page upon success, or displays a limit notification page if the limit is reached.
"""
@login_required
def game_detail(request, game_id):
    game = Game.objects.get(id=game_id, user=request.user)
    return render(request, "generator/game_detail.html", {"game": game})


"""
Displays a dashboard with all games created by the logged-in user.
This view retrieves all games associated with the logged-in user and renders them into a list.
It is accessible only to logged-in users. The dashboard page allows users to view
Args:
    request (HttpRequest): The HTTP request object.
Returns:
    HttpResponse: Renders the dashboard page with the user's games.
"""
@login_required
def dashboard(request):
    games = Game.objects.filter(user=request.user)
    return render(request, "generator/dashboard.html", {"games": games})


def random_game():
    """Génère des mots aléatoires pour pré-remplir le formulaire de jeu."""
    # Chemin vers le fichier de mots
    words_file = os.path.join(settings.STATICFILES_DIRS[0], 'words.txt')

    genres, moods, keywords = [], [], []
    current_section = None
    try:
        with open(words_file, 'r') as f:
            for line in f:
                line = line.strip()
                if line == '[genres]':
                    current_section = genres
                elif line == '[moods]':
                    current_section = moods
                elif line == '[keywords]':
                    current_section = keywords
                elif line and current_section is not None:
                    current_section.append(line)
    except Exception as e:
        print(f"Error reading words file: {e}")
        genres = ['adventure', 'puzzle'] 
        moods = ['happy', 'dark']
        keywords = ['cat', 'forest', 'star']
        
    random_genre = random.choice(genres)
    random_mood = random.choice(moods)
    random_keywords = ', '.join(random.sample(keywords, 3))

    return {
        'genre': random_genre,
        'mood': random_mood,
        'keywords': random_keywords
    }