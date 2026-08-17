from django.http import HttpRequest, HttpResponse
from django.shortcuts import render

from main.forms import SearchForm
from main.models import Music


def search(request: HttpRequest) -> HttpResponse:
    """ 検索結果 """

    search_form = SearchForm(request.GET)
    if search_form.is_valid():
        q = search_form.cleaned_data['q']
    else:
        # 無効な入力は空検索と同じ扱いにする (入力値も再描画しない)
        search_form = SearchForm()
        q = ''

    if q:
        # 大文字小文字区別無しの部分一致
        items = Music.objects.filter(title__icontains=q).order_by('level', '-sran_level', 'title')
    else:
        items = []

    context = {
        'title': '{q} の検索結果'.format(q=q) if q else '楽曲検索',
        'search_form': search_form,
        'q': q,
        'items': items,
        'is_blank': not q
    }
    return render(request, 'main/search.html', context)
