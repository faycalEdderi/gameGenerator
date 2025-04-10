from django import forms

class GameForm(forms.Form):
    genre = forms.CharField(max_length=50, label="Genre du jeu")
    mood = forms.CharField(max_length=50, label="Ambiance")
    keywords = forms.CharField(
        widget=forms.Textarea,
        label="Mots-clés", 
        help_text="Séparez les mots-clés par des virgules.",
        )