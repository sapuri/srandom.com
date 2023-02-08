from main.models import Difficulty, Level, Sran_Level, Music


def create_music(title: str = 'test', difficulty: str = 'EXTRA', level: int = 50, sran_level: int = 19) -> Music:
    difficulty = Difficulty.objects.create(difficulty=difficulty)
    level = Level.objects.create(level=level)
    sran_level = Sran_Level.objects.create(level=sran_level)
    return Music.objects.create(title=title, difficulty=difficulty, level=level, sran_level=sran_level)
