from django.core.management.base import BaseCommand
from octofit_tracker.models import UserProfile, Team, TeamInvitation, Activity
from django.contrib.auth.models import User

class Command(BaseCommand):
    help = 'Populate the octofit_db database with test data'

    def handle(self, *args, **options):
        # Eliminar datos previos
        Activity.objects.all().delete()
        TeamInvitation.objects.all().delete()
        Team.objects.all().delete()
        UserProfile.objects.all().delete()

        # Crear usuarios superhéroes (solo en UserProfile)
        marvel = [
            {'username': 'ironman', 'bio': 'Genio, millonario, filántropo.'},
            {'username': 'spiderman', 'bio': 'Amigable vecino.'},
            {'username': 'captain', 'bio': 'El primer vengador.'},
        ]
        dc = [
            {'username': 'batman', 'bio': 'El caballero de la noche.'},
            {'username': 'superman', 'bio': 'El hombre de acero.'},
            {'username': 'wonderwoman', 'bio': 'Guerrera amazona.'},
        ]
        for u in marvel + dc:
            UserProfile.objects.create(**u)

        # Crear equipos
        team_marvel = Team.objects.create(
            name='Marvel',
            description='Equipo Marvel',
            owner_username='ironman',
            members=['ironman', 'spiderman', 'captain']
        )
        team_dc = Team.objects.create(
            name='DC',
            description='Equipo DC',
            owner_username='batman',
            members=['batman', 'superman', 'wonderwoman']
        )

        # Crear actividades
        for username in ['ironman', 'spiderman', 'captain', 'batman', 'superman', 'wonderwoman']:
            Activity.objects.create(username=username, type='run', distance=5.0, duration='00:30:00', notes='Entrenamiento base')
            Activity.objects.create(username=username, type='bike', distance=10.0, duration='00:45:00', notes='Entrenamiento avanzado')

        # Crear invitaciones
        TeamInvitation.objects.create(team_name='Marvel', invited_username='batman', invited_by_username='ironman', accepted=False)
        TeamInvitation.objects.create(team_name='DC', invited_username='ironman', invited_by_username='batman', accepted=True)

        self.stdout.write(self.style.SUCCESS('Base de datos poblada con datos de ejemplo (Marvel y DC).'))
