from django.shortcuts import get_object_or_404
from django.core.exceptions import ObjectDoesNotExist
from rest_framework import viewsets, filters, permissions
from rest_framework.response import Response
from rest_framework.decorators import detail_route, list_route

from main.models import Music, Medal, Bad_Count
from users.models import CustomUser
from .serializer import MusicSerializer, MedalSerializer, Bad_CountSerializer, CustomUserSerializer

''' Permissions '''
# 管理者のみ Write 可能、その他のユーザは Read のみ
class IsAdminOrReadOnly(permissions.BasePermission):
    def has_permission(self, request, view):
        return permissions.IsAdminUser().has_permission(request, view) or request.method in permissions.SAFE_METHODS

class IsUserOrReadOnly(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return True
        return obj == request.user

class RecordPermissions(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS and obj.cleardata_privacy == 1:
            return True
        else:
            return obj == request.user

''' Main '''
class MusicViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Music.objects.all()
    serializer_class = MusicSerializer
    filter_fields = ('difficulty', 'level', 'sran_level')

''' Users '''
class CustomUserViewSet(viewsets.ModelViewSet):
    permission_classes = (IsUserOrReadOnly,)
    queryset = CustomUser.objects.filter(is_active=True)
    serializer_class = CustomUserSerializer
    filter_fields = ('player_name_privacy', 'cleardata_privacy', 'updated_recently_privacy', 'premium', 'location', 'theme')
    http_method_names = ['get', 'put']

    @detail_route(methods=['get'], url_path='get_record/(?P<music_id>[0-9]+)')
    # TODO: パーミッションを設定する
    def get_record(self, request, pk=None, music_id=None):
        user = get_object_or_404(CustomUser, pk=pk)
        music = get_object_or_404(Music, pk=music_id)

        try:
            medal = Medal.objects.get(music=music, user=user)
        except ObjectDoesNotExist:
            medal = None

        try:
            bad_count = Bad_Count.objects.get(music=music, user=user)
        except ObjectDoesNotExist:
            bad_count = None

        record = {
            'medal': MedalSerializer(medal).data,
            'bad_count': Bad_CountSerializer(bad_count).data
        }
        return Response(record)

    @detail_route(methods=['put'], url_path='update_record/(?P<music_id>[0-9]+)')
    # TODO: パーミッションを設定する
    def update_record(self, request, pk=None, music_id=None):
        # 更新処理
        pass

    @detail_route(methods=['delete'], url_path='delete_record/(?P<music_id>[0-9]+)')
    # TODO: パーミッションを設定する
    def delete_record(self, request, pk=None, music_id=None):
        # 削除処理
        pass
