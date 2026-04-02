from django.urls import path
from .views import hello_from_notes_app, show_product_list, notes_list

urlpatterns = [
    path('hello/', hello_from_notes_app),
    path('show_product_list/', show_product_list),
    path('notes_list/', notes_list, name='notes_list'),
]