from django.conf.urls import include
from django.urls import path
from rest_framework import routers
from .views import MusicViewSet, ActivityViewSet, CustomUserViewSet

router = routers.DefaultRouter()
router.register(r'music', MusicViewSet)
router.register(r'activity', ActivityViewSet)
router.register(r'users', CustomUserViewSet)

app_name = 'api'
urlpatterns = [
    path('', include(router.urls)),
]
