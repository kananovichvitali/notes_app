from django.http import HttpResponse
from django.shortcuts import render
from .models import *

def hello_from_notes_app(request):
    return HttpResponse("Hello from Notes app")

def show_product_list(request):
    products = [
        {
            "name": "Banana",
            "price": 10,
            "description": "fruit"
        },
        {
            "name": "Apple",
            "price": 8,
            "description": "fruit"
        },
        {
            "name": "Carrot",
            "price": 2,
            "description": "vegetable"
        }
    ]
    return render(request, 'index.html', {'products': products})


def notes_list(request):
    all_notes = Note.objects.all()
    return render(request, 'notes_list.html', {'notes': all_notes})