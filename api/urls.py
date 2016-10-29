from django.conf.urls import include, url
from rest_framework import routers
from .views import MusicViewSet, ActivityViewSet, CustomUserViewSet

router = routers.DefaultRouter()
router.register(r'music', MusicViewSet)
router.register(r'activity', ActivityViewSet)
router.register(r'users', CustomUserViewSet)

app_name = 'api'
urlpatterns = [
    url('', include(router.urls)),
]
