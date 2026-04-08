from django.db import models
from django.urls import reverse
from django.contrib.auth.models import User
from django.utils import timezone

class Category(models.Model):
    title = models.CharField(max_length=100, verbose_name="Назва категорії")

    def __str__(self):
        return self.title

class Note(models.Model):
    title = models.CharField(max_length=100, verbose_name="Що зробити?")
    text = models.TextField(verbose_name="Деталі завдання")
    reminder = models.DateTimeField(null=True, blank=True, verbose_name="Коли виконати (нагадування)")
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='notes', verbose_name="Категорія")
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='notes', verbose_name="Автор")
    remind_at = models.DateTimeField(null=True, blank=True, verbose_name="Коли нагадати?")
    is_sent = models.BooleanField(default=False)

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('note_detail', args=[self.pk])