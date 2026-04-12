from django.http import HttpResponse
from django.shortcuts import render, redirect
from .models import *
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.mixins import LoginRequiredMixin
from .forms import NoteForm, LoginForm, RegisterForm
from django.urls import reverse_lazy
from django.views.generic import CreateView, DetailView, ListView, UpdateView, DeleteView
import time
import httpx
import asyncio
import aiohttp
from django.http import JsonResponse
from django.views import View
from django.shortcuts import render
from asgiref.sync import sync_to_async
from .models import Note, Category
from django.contrib.auth.models import User

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


class NoteListView(LoginRequiredMixin, ListView):
    model = Note
    template_name = 'note_list.html'
    context_object_name = 'notes'

    def get_queryset(self):
        queryset = Note.objects.filter(author=self.request.user)
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


class NoteCreateView(LoginRequiredMixin, CreateView):
    model = Note
    form_class = NoteForm
    template_name = 'note_form.html'
    success_url = reverse_lazy('note_list')

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)

class NoteDetailView(LoginRequiredMixin, DetailView):
    model = Note
    template_name = 'note_detail.html'

    def get_queryset(self):
        return Note.objects.filter(author=self.request.user)

class NoteUpdateView(LoginRequiredMixin, UpdateView):
    model = Note
    form_class = NoteForm
    template_name = 'note_form.html'
    success_url = reverse_lazy('note_list')

    def get_queryset(self):
        return Note.objects.filter(author=self.request.user)

class NoteDeleteView(LoginRequiredMixin, DeleteView):
    model = Note
    template_name = 'note_confirm_delete.html'
    success_url = reverse_lazy('note_list')

    def get_queryset(self):
        return Note.objects.filter(author=self.request.user)

def login_view(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            user = authenticate(username=form.cleaned_data['username'], password=form.cleaned_data['password'])
            if user:
                login(request, user)
                messages.success(request, f"Вітаємо, {user.username}!")
                return redirect('note_list')
            messages.error(request, "Невірне ім'я або пароль")
    else:
        form = LoginForm()
    return render(request, 'login.html', {'form': form})

def register_view(request):
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('note_list')
    else:
        form = RegisterForm()
    return render(request, 'register.html', {'form': form})

def logout_view(request):
    logout(request)
    return redirect('login')



TODO_IDS = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]

class SyncNoteImportView(View):
    def get(self, request):
        return render(request, 'note_import.html', {'view_type': 'sync'})

    def post(self, request):
        start_time = time.time()
        results = []

        user = User.objects.first()
        category = Category.objects.first()

        for todo_id in TODO_IDS:
            try:
                with httpx.Client() as client:
                    response = client.get(f'https://jsonplaceholder.typicode.com/todos/{todo_id}')
                    if response.status_code == 200:
                        data = response.json()
                        note, created = Note.objects.get_or_create(
                            title=data.get('title')[:100],
                            author=user,
                            category=category,
                            defaults={'text': f"Імпортоване завдання №{todo_id}"}
                        )
                        results.append({'id': todo_id, 'status': 'created' if created else 'exists'})
            except Exception as e:
                print(f"Error: {e}")

        execution_time = time.time() - start_time
        return JsonResponse({'type': 'sync', 'execution_time': round(execution_time, 2), 'count': len(results)})


class AsyncNoteImportView(View):
    async def get(self, request):
        return render(request, 'note_import.html', {'view_type': 'async'})

    async def post(self, request):
        start_time = time.time()

        user = await sync_to_async(User.objects.first)()
        category = await sync_to_async(Category.objects.first)()

        async def fetch_and_save(session, todo_id):
            url = f'https://jsonplaceholder.typicode.com/todos/{todo_id}'
            async with session.get(url) as response:
                if response.status == 200:
                    data = await response.json()
                    note, created = await sync_to_async(Note.objects.get_or_create)(
                        title=data.get('title')[:100],
                        author=user,
                        category=category,
                        defaults={'text': f"Асинхронне імпортування №{todo_id}"}
                    )
                    return {'id': todo_id, 'created': created}
                return {'error': response.status}

        async with aiohttp.ClientSession() as session:
            tasks = [fetch_and_save(session, tid) for tid in TODO_IDS]
            results = await asyncio.gather(*tasks)

        execution_time = time.time() - start_time
        return JsonResponse({'type': 'async', 'execution_time': round(execution_time, 2), 'count': len(results)})


class HttpClientComparisonView(View):
    async def get(self, request):
        return render(request, 'http_comparison.html')

    async def post(self, request):
        client_type = request.POST.get('client_type', 'httpx_sync')
        start_time = time.time()

        if client_type == 'httpx_sync':
            results = await self._test_httpx_sync()
        elif client_type == 'httpx_async':
            results = await self._test_httpx_async()

        execution_time = time.time() - start_time
        return JsonResponse({
            'client_type': client_type,
            'execution_time': round(execution_time, 2),
            'results_count': len(results)
        })

    async def _test_httpx_sync(self):
        def run():
            res = []
            with httpx.Client() as client:
                for tid in TODO_IDS:
                    client.get(f'https://jsonplaceholder.typicode.com/todos/{tid}')
                    res.append(tid)
            return res

        return await sync_to_async(run)()

    async def _test_httpx_async(self):
        async with httpx.AsyncClient() as client:
            tasks = [client.get(f'https://jsonplaceholder.typicode.com/todos/{tid}') for tid in TODO_IDS]
            return await asyncio.gather(*tasks)