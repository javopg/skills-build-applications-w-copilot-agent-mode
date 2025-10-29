from djongo import models
from rest_framework import serializers
from .models import UserProfile, Team, TeamInvitation, Activity

class UserProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserProfile
        fields = ['user', 'bio', 'avatar']

class TeamSerializer(serializers.ModelSerializer):
    class Meta:
        model = Team
        fields = ['name', 'description', 'owner', 'members', 'created_at']

class TeamInvitationSerializer(serializers.ModelSerializer):
    class Meta:
        model = TeamInvitation
        fields = ['team', 'invited_user', 'invited_by', 'accepted', 'created_at']

class ActivitySerializer(serializers.ModelSerializer):
    class Meta:
        model = Activity
        fields = ['user', 'type', 'distance', 'duration', 'date', 'notes']
