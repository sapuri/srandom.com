from users.models import Location, Theme, CustomUser


def create_user(username: str = 'test', location: str = 'test', theme: str = 'test', premium: bool = False) -> CustomUser:
    location = Location.objects.create(location=location)
    theme = Theme.objects.create(theme=theme)
    return CustomUser.objects.create_user(username, location=location, theme=theme, premium=premium)
