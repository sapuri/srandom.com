from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.shortcuts import render

from users.models import CustomUser


def list_users(request):
    """ ユーザーリスト """
    # 有効なアカウントを取得
    users = CustomUser.objects.filter(
        is_active=True).exclude(pk=1).order_by('id')

    # ページング
    paginator = Paginator(users, 50)
    page = request.GET.get('page')

    try:
        users = paginator.page(page)
    except PageNotAnInteger:
        # If page is not an integer, deliver first page.
        users = paginator.page(1)
    except EmptyPage:
        # If page is out of range (e.g. 9999), deliver last page of results.
        users = paginator.page(paginator.num_pages)

    context = {'users': users}
    return render(request, 'users/list.html', context)
