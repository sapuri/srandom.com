from django.core.paginator import Paginator
from django.http import HttpRequest, HttpResponse
from django.shortcuts import render

from users.models import CustomUser


def list_users(request: HttpRequest) -> HttpResponse:
    """ ユーザーリスト """

    users = CustomUser.objects.filter(is_active=True).exclude(pk=1).order_by('id')

    paginator = Paginator(users, 50)
    page = request.GET.get('page')
    users = paginator.get_page(page)

    context = {'users': users}
    return render(request, 'users/list.html', context)
