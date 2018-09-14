from django.conf import settings
from django.conf.urls import include
from django.urls import path
from django.contrib import admin

urlpatterns = [
    path('', include('main.urls')),
    path('mastermind/', admin.site.urls),
    path('auth/', include(('django.contrib.auth.urls', 'auth'))),
    path('social/', include(('social_django.urls', 'social'))),
    path('users/', include('users.urls')),
]

if settings.DEBUG:
    import debug_toolbar
    urlpatterns = [
        path('__debug__/', include(debug_toolbar.urls)),
    ] + urlpatterns
