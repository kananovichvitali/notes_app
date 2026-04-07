import pytest
from ..forms import NoteForm
from .factories import CategoryFactory

@pytest.mark.django_db
def test_note_form_valid():
    category = CategoryFactory()
    form_data = {
        'title': 'Купити молоко',
        'text': 'Треба купити 2 літри молока',
        'category': category.id
    }
    form = NoteForm(data=form_data)
    assert form.is_valid(), form.errors

@pytest.mark.django_db
def test_note_form_with_invalid_empty_title():
    form_data = {
        'title': '',
        'text': 'Якийсь прикладовий текст'
    }
    form = NoteForm(data=form_data)
    assert not form.is_valid()
    assert 'title' in form.errors