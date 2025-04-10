from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .forms import GameForm
from .utils import generate_game
from .models import Game

@login_required
def create_game(request):
    if request.method == "POST":
        form = GameForm(request.POST)
        if form.is_valid():
            data = form.cleaned_data
            game_data = generate_game(data["genre"], data["mood"], data["keywords"])
            game = Game.objects.create(
                user=request.user,
                title=f"Jeu {data['genre']} - {data['mood']}",
                genre=data["genre"],
                mood=data["mood"],
                keywords=data["keywords"],
                story=game_data["story"],
                characters=game_data["characters"],
                locations=game_data["locations"]
            )
            return redirect("game_detail", game_id=game.id)
    else:
        form = GameForm()
    return render(request, "generator/create_game.html", {"form": form})

@login_required
def game_detail(request, game_id):
    game = Game.objects.get(id=game_id, user=request.user)
    return render(request, "generator/game_detail.html", {"game": game})

@login_required
def dashboard(request):
    games = Game.objects.filter(user=request.user)
    return render(request, "generator/dashboard.html", {"games": games})