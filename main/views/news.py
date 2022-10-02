from django.http import HttpRequest, HttpResponse
from django.shortcuts import render

from main.models import News


def news(request: HttpRequest) -> HttpResponse:
    """ NEWS """

    news = News.objects.filter(status=True).order_by('-id')

    context = {
        'news': news,
    }
    return render(request, 'main/news.html', context)
