from django.http import HttpResponse
from django.shortcuts import render

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