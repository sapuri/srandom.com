from django.contrib import admin
from .models import *


class LocationAdmin(admin.ModelAdmin):
    list_display = ('id', 'location')
    ordering = ('id',)


class ThemeAdmin(admin.ModelAdmin):
    list_display = ('id', 'theme')
    ordering = ('id',)


class CustomUserAdmin(admin.ModelAdmin):
    list_display = ('id', 'username', 'first_name', 'email', 'is_active', 'last_login',
                    'date_joined', 'player_name', 'poputomo_id', 'location', 'theme', 'premium')
    list_filter = ('is_active', 'location', 'theme', 'premium')
    ordering = ('id',)


admin.site.register(Location, LocationAdmin)
admin.site.register(Theme, ThemeAdmin)
admin.site.register(CustomUser, CustomUserAdmin)
