from django.contrib import admin
from .models import Location, CustomUser

class LocationAdmin(admin.ModelAdmin):
    list_display = ('id', 'location')
    ordering = ('id',)

class CustomUserAdmin(admin.ModelAdmin):
    list_display = ('id', 'username', 'first_name', 'email', 'is_active', 'last_login', 'date_joined', 'player_name', 'poputomo_id', 'location', 'premium')
    ordering = ('id',)

admin.site.register(Location, LocationAdmin)
admin.site.register(CustomUser, CustomUserAdmin)
