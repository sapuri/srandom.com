from django.shortcuts import render


def premium(request):
    """ プレミアムユーザー """
    return render(request, 'main/premium.html')
