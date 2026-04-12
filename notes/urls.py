from django.urls import path
from .views import *

urlpatterns = [
    # path('hello/', hello_from_notes_app),
    # path('show_product_list/', show_product_list),
    # path('notes_list/', notes_list, name='notes_list'),
    path('', NoteListView.as_view(), name='note_list'),
    path('create/', NoteCreateView.as_view(), name='note_create'),
    path('<int:pk>/', NoteDetailView.as_view(), name='note_detail'),
    path('<int:pk>/edit/', NoteUpdateView.as_view(), name='note_edit'),
    path('<int:pk>/delete/', NoteDeleteView.as_view(), name='note_delete'),
    path('login/', login_view, name='login'),
    path('register/', register_view, name='register'),
    path('logout/', logout_view, name='logout'),
    path('import/sync/', SyncNoteImportView.as_view(), name='sync_import'),
    path('import/async/', AsyncNoteImportView.as_view(), name='async_import'),
    path('import/comparison/', HttpClientComparisonView.as_view(), name='http_comparison'),
]