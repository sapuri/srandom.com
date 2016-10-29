from django.shortcuts import get_object_or_404
from django.core.exceptions import ObjectDoesNotExist
from rest_framework import viewsets, filters, permissions
from rest_framework.response import Response
from rest_framework.decorators import detail_route, list_route
from django_filters.rest_framework import DjangoFilterBackend

from main.models import Music, Medal, Bad_Count, Extra_Option, Activity
from users.models import CustomUser
from .serializer import MusicSerializer, CustomUserSerializer, MedalSerializer, Bad_CountSerializer, Extra_OptionSerializer, ActivitySerializer

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
    filter_backends = (DjangoFilterBackend, filters.OrderingFilter)
    filter_fields = ('level', 'sran_level')
    ordering_fields = ('title', 'level', 'sran_level')

class ActivityViewSet(viewsets.ModelViewSet):
    permission_classes = (IsUserOrReadOnly,)
    queryset = Activity.objects.all()
    serializer_class = ActivitySerializer
    filter_fields = ('music', 'user', 'updated_at', 'status')

''' Users '''
class CustomUserViewSet(viewsets.ModelViewSet):
    permission_classes = (IsUserOrReadOnly, permissions.IsAuthenticated)
    queryset = CustomUser.objects.filter(is_active=True)
    serializer_class = CustomUserSerializer
    filter_fields = ('player_name_privacy', 'cleardata_privacy', 'updated_recently_privacy', 'premium', 'location', 'theme')
    http_method_names = ['get', 'put']

    @list_route()
    def my_account(self, request):
        serializer = CustomUserSerializer(request.user)
        return Response(serializer.data)

    @detail_route(methods=['get'], url_path='record/(?P<music_id>[0-9]+)')
    # TODO: パーミッションを設定する
    def get_record(self, request, pk=None, music_id=None):
        user = get_object_or_404(CustomUser, username=pk)
        music = get_object_or_404(Music, pk=music_id)

        try:
            medal = Medal.objects.get(music=music, user=user)
        except ObjectDoesNotExist:
            medal = None

        try:
            bad_count = Bad_Count.objects.get(music=music, user=user)
        except ObjectDoesNotExist:
            bad_count = None

        try:
            extra_option = Extra_Option.objects.get(music=music, user=user)
        except ObjectDoesNotExist:
            extra_option = None

        record = {
            'music': MusicSerializer(music).data,
            'medal': MedalSerializer(medal).data,
            'bad_count': Bad_CountSerializer(bad_count).data,
            'extra_option': Extra_OptionSerializer(extra_option).data
        }
        return Response(record)

    @detail_route(methods=['put'], url_path='record/update/(?P<music_id>[0-9]+)')
    # TODO: パーミッションを設定する
    def update_record(self, request, pk=None, music_id=None):
        # 更新処理
        pass

    @detail_route(methods=['delete'], url_path='record/delete/(?P<music_id>[0-9]+)')
    # TODO: パーミッションを設定する
    def delete_record(self, request, pk=None, music_id=None):
        # 削除処理
        pass
