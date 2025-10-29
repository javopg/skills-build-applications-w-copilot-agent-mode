"""octofit_tracker URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import ActivityViewSet, TeamViewSet, TeamInvitationViewSet, LeaderboardView, TrainingSuggestionView
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.reverse import reverse
import os


router = DefaultRouter()
router.register(r'activities', ActivityViewSet, basename='activity')
router.register(r'teams', TeamViewSet, basename='team')
router.register(r'invitations', TeamInvitationViewSet, basename='invitation')


@api_view(['GET'])
def api_root(request, format=None):
    codespace_name = os.environ.get('CODESPACE_NAME')
    base_url = request.build_absolute_uri('/')
    if codespace_name:
        base_url = f"https://{codespace_name}-8000.app.github.dev/api/"
    else:
        base_url = base_url.rstrip('/') + '/api/'
    return Response({
        'teams': base_url + 'teams/',
        'activities': base_url + 'activities/',
        'leaderboard': base_url + 'leaderboard/',
        'suggestions': base_url + 'suggestions/',
    })


urlpatterns = [
    path('', api_root, name='api-root'),
    path('admin/', admin.site.urls),
    # Endpoints REST para autenticación y registro
    path('api/auth/', include('dj_rest_auth.urls')),
    path('api/auth/registration/', include('dj_rest_auth.registration.urls')),
    # Endpoints REST para actividades
    path('api/', include(router.urls)),
    # Endpoint para leaderboard competitivo
    path('api/leaderboard/', LeaderboardView.as_view(), name='leaderboard'),
    # Endpoint para sugerencias de entrenamiento personalizadas
    path('api/suggestions/', TrainingSuggestionView.as_view(), name='suggestions'),
]
