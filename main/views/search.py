from django.http import HttpRequest, HttpResponse
from django.shortcuts import render

from main.forms import SearchForm
from main.models import Music


def search(request: HttpRequest) -> HttpResponse:
    """ 検索結果 """

    def search_items(q: str = None) -> list[Music]:
        filter_params = {}
        if q:
            # 大文字小文字区別無しの部分一致
            filter_params['title__icontains'] = q
        return Music.objects.filter(**filter_params).order_by('level', '-sran_level', 'title')

    search_form = SearchForm(request.GET)
    if search_form.is_valid():
        q = search_form.cleaned_data['q']
        if q:
            is_blank = False
            items = search_items(q=q)
        else:
            is_blank = True
            items = []
    else:
        is_blank = True
        items = []

    context = {
        'title': '{q} の検索結果'.format(q=q) if not is_blank else '楽曲検索',
        'search_form': search_form,
        'q': q,
        'items': items,
        'is_blank': is_blank
    }
    return render(request, 'main/search.html', context)
