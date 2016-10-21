from rest_framework import serializers

from main.models import *
from users.models import *

''' Main '''
class DifficultySerializer(serializers.ModelSerializer):
    class Meta:
        model = Difficulty
        fields = '__all__'

class LevelSerializer(serializers.ModelSerializer):
    class Meta:
        model = Level
        fields = '__all__'

class Sran_LevelSerializer(serializers.ModelSerializer):
    class Meta:
        model = Sran_Level
        fields = '__all__'

class MusicSerializer(serializers.ModelSerializer):
    difficulty = DifficultySerializer()
    level = LevelSerializer()
    sran_level = Sran_LevelSerializer()

    class Meta:
        model = Music
        fields = '__all__'

''' Users '''
class LocationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Location
        fields = '__all__'

class ThemeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Theme
        fields = '__all__'

class CustomUserSerializer(serializers.ModelSerializer):
    location = LocationSerializer()
    theme = ThemeSerializer()

    class Meta:
        model = CustomUser
        fields = (
            'id',
            'username',
            'player_name',
            'poputomo_id',
            'profile',
            'player_name_privacy',
            'cleardata_privacy',
            'updated_recently_privacy',
            'premium',
            'location',
            'theme'
        )

class MedalSerializer(serializers.ModelSerializer):
    music = MusicSerializer()
    user = CustomUserSerializer()

    class Meta:
        model = Medal
        fields = '__all__'

class Bad_CountSerializer(serializers.ModelSerializer):
    music = MusicSerializer()
    user = CustomUserSerializer()

    class Meta:
        model = Bad_Count
        fields = '__all__'
