from django.urls import path
from . import views

urlpatterns = [
    path('', views.dashboard, name='dashboard'),
    path('create/', views.create_game, name='create_game'),
    path('game/<int:game_id>/', views.game_detail, name='game_detail'),
]