from django.contrib import admin
from .models import Difficulty, Level, Sran_Level, Music, Medal, Bad_Count, Extra_Option

class DifficultyAdmin(admin.ModelAdmin):
    list_display = ('id', 'difficulty')
    ordering = ('id',)

class LevelAdmin(admin.ModelAdmin):
    list_display = ('id', 'level')
    ordering = ('id',)

class Sran_LevelAdmin(admin.ModelAdmin):
    list_display = ('id', 'level')
    ordering = ('id',)

class MusicAdmin(admin.ModelAdmin):
    list_display = ('id', 'title', 'difficulty', 'level', 'sran_level', 'bpm')
    ordering = ('id',)

class MedalAdmin(admin.ModelAdmin):
    list_display = ('id', 'medal', 'music', 'user', 'updated_at')
    ordering = ('-id',)

class Bad_CountAdmin(admin.ModelAdmin):
    list_display = ('id', 'bad_count', 'music', 'user', 'updated_at')
    ordering = ('-id',)

class Extra_OptionAdmin(admin.ModelAdmin):
    list_display = ('id', 'hard', 'music', 'user', 'updated_at')
    ordering = ('-id',)

admin.site.register(Difficulty, DifficultyAdmin)
admin.site.register(Level, LevelAdmin)
admin.site.register(Sran_Level, Sran_LevelAdmin)
admin.site.register(Music, MusicAdmin)
admin.site.register(Medal, MedalAdmin)
admin.site.register(Bad_Count, Bad_CountAdmin)
admin.site.register(Extra_Option, Extra_OptionAdmin)
