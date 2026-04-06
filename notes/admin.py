from django.contrib import admin
from .models import Note, Category

@admin.register(Note)
class NoteAdmin(admin.ModelAdmin):
    list_display = ('title', 'author', 'category', 'reminder')
    list_filter = ('author', 'category')
    search_fields = ('title', 'text')

admin.site.register(Category)
