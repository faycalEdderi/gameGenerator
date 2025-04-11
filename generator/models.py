from django.db import models
from django.contrib.auth.models import User

class Game(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=100)
    genre = models.CharField(max_length=50)
    mood = models.CharField(max_length=50)
    keywords = models.TextField()
    story = models.TextField()
    characters = models.TextField()
    locations = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    image = models.ImageField(upload_to='game_images/', blank=True, null=True)

    def __str__(self):
        return self.title
    
    
class Word(models.Model):
    CATEGORY_CHOICES = [
        ('genre', 'Genre'),
        ('mood', 'Mood'),
        ('keyword', 'Keyword'),
    ]
    category = models.CharField(max_length=20, choices=CATEGORY_CHOICES)
    word = models.CharField(max_length=50, unique=True)

    def __str__(self):
        return f"{self.word} ({self.category})"