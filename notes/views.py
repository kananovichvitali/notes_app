from django.http import HttpResponse
from django.shortcuts import render
from .models import *
from django.db.models import Q
from .forms import NoteForm
from django.urls import reverse_lazy
from django.views.generic import CreateView, DetailView, ListView, UpdateView, DeleteView

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


class NoteListView(ListView):
    model = Note
    template_name = 'note_list.html'
    context_object_name = 'notes'

    def get_queryset(self):
        queryset = super().get_queryset()
        search_query = self.request.GET.get('search')
        category_id = self.request.GET.get('category')

        if search_query:
            queryset = queryset.filter(title__icontains=search_query)

        if category_id:
            queryset = queryset.filter(category_id=category_id)

        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['categories'] = Category.objects.all()
        return context


class NoteCreateView(CreateView):
    model = Note
    form_class = NoteForm
    template_name = 'note_form.html'
    success_url = reverse_lazy('note_list')


class NoteDetailView(DetailView):
    model = Note
    template_name = 'note_detail.html'


class NoteUpdateView(UpdateView):
    model = Note
    form_class = NoteForm
    template_name = 'note_form.html'
    success_url = reverse_lazy('note_list')


class NoteDeleteView(DeleteView):
    model = Note
    template_name = 'note_confirm_delete.html'
    success_url = reverse_lazy('note_list')

