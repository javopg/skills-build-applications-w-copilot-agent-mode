from django.db import models
from django.contrib.auth.models import User

class Activity(models.Model):
    ACTIVITY_TYPES = [
        ('run', 'Correr'),
        ('bike', 'Bicicleta'),
        ('swim', 'Natación'),
        ('walk', 'Caminar'),
        # Puedes agregar más tipos
    ]
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='activities')
    type = models.CharField(max_length=20, choices=ACTIVITY_TYPES)
    distance = models.FloatField(help_text='Distancia en kilómetros')
    duration = models.DurationField(help_text='Duración de la actividad')
    date = models.DateTimeField(auto_now_add=True)
    notes = models.TextField(blank=True)

    def __str__(self):
        return f"{self.user.username} - {self.type} ({self.date.date()})"
