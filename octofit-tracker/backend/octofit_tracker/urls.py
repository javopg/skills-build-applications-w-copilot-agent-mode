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


router = DefaultRouter()
router.register(r'activities', ActivityViewSet, basename='activity')
router.register(r'teams', TeamViewSet, basename='team')
router.register(r'invitations', TeamInvitationViewSet, basename='invitation')


@api_view(['GET'])
def api_root(request, format=None):
    return Response({
        'users': reverse('user-list', request=request, format=format),
        'teams': reverse('team-list', request=request, format=format),
        'activities': reverse('activity-list', request=request, format=format),
        'leaderboard': reverse('leaderboard', request=request, format=format),
        'suggestions': reverse('suggestions', request=request, format=format),
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
