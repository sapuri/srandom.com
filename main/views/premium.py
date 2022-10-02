from django.http import HttpRequest, HttpResponse
from django.shortcuts import render


def premium(request: HttpRequest) -> HttpResponse:
    """ プレミアムユーザー """

    return render(request, 'main/premium.html')
