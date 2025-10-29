from djongo import models
from django.contrib import admin
from .models import UserProfile, Team, TeamInvitation, Activity

@admin.register(UserProfile)
class UserProfileAdmin(admin.ModelAdmin):
    list_display = ('username', 'bio')

@admin.register(Team)
class TeamAdmin(admin.ModelAdmin):
    list_display = ('name', 'owner_username', 'created_at', 'members')

@admin.register(TeamInvitation)
class TeamInvitationAdmin(admin.ModelAdmin):
    list_display = ('team_name', 'invited_username', 'invited_by_username', 'accepted', 'created_at')

@admin.register(Activity)
class ActivityAdmin(admin.ModelAdmin):
    list_display = ('username', 'type', 'distance', 'duration', 'date')
