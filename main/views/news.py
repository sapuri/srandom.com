from django.shortcuts import render

from main.models import News


def news(request):
    """ NEWS """
    news = News.objects.filter(status=True).order_by('-id')

    context = {
        'news': news,
    }
    return render(request, 'main/news.html', context)
