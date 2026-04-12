import pytest
from ..forms import NoteForm
from .factories import CategoryFactory

@pytest.mark.django_db
def test_note_form_valid():
    category = CategoryFactory()
    form_data = {
        'title': 'Купити продукти',
        'text': 'Молоко, хліб, сир',
        'category': category.id
    }
    form = NoteForm(data=form_data)
    assert form.is_valid()


@pytest.mark.django_db
def test_note_form_invalid_empty_fields():
    form = NoteForm(data={'title': '', 'text': ''})
    assert not form.is_valid()
    assert 'title' in form.errors
    assert 'text' in form.errors


@pytest.mark.django_db
def test_note_form_title_max_length():
    category = CategoryFactory()
    long_title = "A" * 101
    form_data = {
        'title': long_title,
        'text': 'Тест довгого заголовку',
        'category': category.id
    }
    form = NoteForm(data=form_data)
    assert not form.is_valid()
    assert 'title' in form.errors


@pytest.mark.django_db
def test_note_form_optional_fields():
    category = CategoryFactory()
    form_data = {
        'title': 'Замітка без дати',
        'text': 'Звичайний текст',
        'category': category.id,
        'reminder': ''
    }
    form = NoteForm(data=form_data)
    assert form.is_valid()