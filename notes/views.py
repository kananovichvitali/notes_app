from django.http import HttpResponse

def hello_from_notes_app(request):
    return HttpResponse("Hello from Notes app")