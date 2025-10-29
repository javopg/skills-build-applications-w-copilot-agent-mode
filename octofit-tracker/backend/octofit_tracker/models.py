from django.contrib.auth.models import User
from djongo import models

class UserProfile(models.Model):
    username = models.CharField(max_length=150, unique=True)
    bio = models.TextField(blank=True)
    avatar = models.ImageField(upload_to='avatars/', blank=True, null=True)
    # Puedes agregar más campos personalizados aquí

    def __str__(self):
        return f"Perfil de {self.username}"

class Activity(models.Model):
    ACTIVITY_TYPES = [
        ('run', 'Correr'),
        ('bike', 'Bicicleta'),
        ('swim', 'Natación'),
        ('walk', 'Caminar'),
        # Puedes agregar más tipos
    ]
    username = models.CharField(max_length=150)
    type = models.CharField(max_length=20, choices=ACTIVITY_TYPES)
    distance = models.FloatField(help_text='Distancia en kilómetros')
    duration = models.CharField(max_length=20, help_text='Duración de la actividad')
    date = models.DateTimeField(auto_now_add=True)
    notes = models.TextField(blank=True)

    def __str__(self):
        return f"{self.username} - {self.type} ({self.date.date()})"

class Team(models.Model):
    name = models.CharField(max_length=100, unique=True)
    description = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    owner_username = models.CharField(max_length=150)
    members = models.JSONField(default=list, blank=True)

    def __str__(self):
        return self.name

class TeamInvitation(models.Model):
    team_name = models.CharField(max_length=100)
    invited_username = models.CharField(max_length=150)
    invited_by_username = models.CharField(max_length=150)
    created_at = models.DateTimeField(auto_now_add=True)
    accepted = models.BooleanField(default=False)

    def __str__(self):
        return f"Invitación a {self.invited_username} para unirse a {self.team_name}"
