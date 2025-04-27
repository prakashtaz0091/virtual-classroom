from django.shortcuts import render


def not_authorized(request):
    return render(request, 'common/not_authorized.html')