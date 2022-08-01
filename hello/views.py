from django.http import HttpResponse


def index(request):
    return HttpResponse("docker.io가 뭔가요")