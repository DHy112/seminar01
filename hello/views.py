from django.http import HttpResponse


def index(request):
    return HttpResponse("코코화이팅")