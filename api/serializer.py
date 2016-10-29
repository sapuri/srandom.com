from rest_framework import serializers

from main.models import *
from users.models import *

class DifficultySerializer(serializers.ModelSerializer):
    class Meta:
        model = Difficulty
        fields = ('difficulty', 'difficulty_short')

class LevelSerializer(serializers.ModelSerializer):
    class Meta:
        model = Level
        fields = ('level',)

class Sran_LevelSerializer(serializers.ModelSerializer):
    class Meta:
        model = Sran_Level
        fields = ('level',)

class MusicSerializer(serializers.ModelSerializer):
    difficulty = DifficultySerializer()
    level = LevelSerializer()
    sran_level = Sran_LevelSerializer()

    class Meta:
        model = Music
        fields = '__all__'

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
    updated_at_jst = serializers.DateTimeField(format='%Y/%-m/%d %-H:%M')

    class Meta:
        model = Medal
        fields = ('medal', 'updated_at_jst')

class Bad_CountSerializer(serializers.ModelSerializer):
    updated_at_jst = serializers.DateTimeField(format='%Y/%-m/%d %-H:%M')

    class Meta:
        model = Bad_Count
        fields = ('bad_count', 'updated_at_jst')

class Extra_OptionSerializer(serializers.ModelSerializer):
    updated_at_jst = serializers.DateTimeField(format='%Y/%-m/%d %-H:%M')

    class Meta:
        model = Extra_Option
        fields = ('hard', 'updated_at_jst')

class ActivitySerializer(serializers.ModelSerializer):
    music = MusicSerializer()
    user = CustomUserSerializer()

    class Meta:
        model = Activity
        fields = '__all__'
