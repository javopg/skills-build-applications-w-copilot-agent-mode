from rest_framework import viewsets, permissions, status
from rest_framework.response import Response
from rest_framework.decorators import action
from .models import Activity, Team, TeamInvitation
from .serializers import ActivitySerializer, TeamSerializer, TeamInvitationSerializer
from django.contrib.auth.models import User
from rest_framework.views import APIView
from django.db.models import Sum
from rest_framework.permissions import IsAuthenticated

class ActivityViewSet(viewsets.ModelViewSet):
    queryset = Activity.objects.all()
    serializer_class = ActivitySerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        # Solo mostrar actividades del usuario autenticado
        return Activity.objects.filter(user=self.request.user)

    def perform_create(self, serializer):
        # Asignar el usuario autenticado al crear la actividad
        serializer.save(user=self.request.user)

    @action(detail=False, methods=['get'])
    def recent(self, request):
        # Endpoint personalizado para actividades recientes
        recent_activities = self.get_queryset().order_by('-date')[:10]
        serializer = self.get_serializer(recent_activities, many=True)
        return Response(serializer.data)

class TeamViewSet(viewsets.ModelViewSet):
    queryset = Team.objects.all()
    serializer_class = TeamSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        # Solo mostrar equipos donde el usuario es miembro o propietario
        return Team.objects.filter(members=self.request.user) | Team.objects.filter(owner=self.request.user)

    def perform_create(self, serializer):
        team = serializer.save(owner=self.request.user)
        team.members.add(self.request.user)

    @action(detail=True, methods=['post'])
    def invite(self, request, pk=None):
        team = self.get_object()
        username = request.data.get('username')
        try:
            invited_user = User.objects.get(username=username)
        except User.DoesNotExist:
            return Response({'error': 'Usuario no encontrado.'}, status=status.HTTP_404_NOT_FOUND)
        if team.members.filter(id=invited_user.id).exists():
            return Response({'error': 'El usuario ya es miembro.'}, status=status.HTTP_400_BAD_REQUEST)
        invitation = TeamInvitation.objects.create(team=team, invited_user=invited_user, invited_by=request.user)
        return Response(TeamInvitationSerializer(invitation).data, status=status.HTTP_201_CREATED)

class TeamInvitationViewSet(viewsets.ModelViewSet):
    queryset = TeamInvitation.objects.all()
    serializer_class = TeamInvitationSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        # Solo invitaciones recibidas por el usuario
        return TeamInvitation.objects.filter(invited_user=self.request.user)

    @action(detail=True, methods=['post'])
    def accept(self, request, pk=None):
        invitation = self.get_object()
        if invitation.accepted:
            return Response({'error': 'La invitación ya fue aceptada.'}, status=status.HTTP_400_BAD_REQUEST)
        invitation.accepted = True
        invitation.team.members.add(invitation.invited_user)
        invitation.save()
        return Response({'status': 'Invitación aceptada.'})

class LeaderboardView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        # Ranking de equipos por distancia total
        teams = Team.objects.all()
        leaderboard = []
        for team in teams:
            total_distance = Activity.objects.filter(user__in=team.members.all()).aggregate(Sum('distance'))['distance__sum'] or 0
            leaderboard.append({
                'team': team.name,
                'members': [user.username for user in team.members.all()],
                'total_distance': total_distance
            })
        # Ordenar por distancia descendente
        leaderboard.sort(key=lambda x: x['total_distance'], reverse=True)
        return Response(leaderboard)

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from .models import Activity, UserProfile
from django.contrib.auth.models import User
import datetime

class TrainingSuggestionView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        user = request.user
        profile = getattr(user, 'profile', None)
        last_activities = Activity.objects.filter(user=user).order_by('-date')[:5]
        suggestions = []
        # Lógica simple basada en historial y perfil
        if last_activities:
            last_type = last_activities[0].type
            if last_type == 'run':
                suggestions.append('Prueba una sesión de bicicleta para variar el entrenamiento.')
            elif last_type == 'bike':
                suggestions.append('Haz una caminata ligera para recuperación activa.')
            else:
                suggestions.append('Intenta una rutina de fuerza o estiramientos.')
        else:
            suggestions.append('Comienza con una caminata suave para activar tu cuerpo.')
        # Personalización por bio
        if profile and profile.bio:
            suggestions.append(f"Tip personalizado: {profile.bio}")
        return Response({'suggestions': suggestions})
