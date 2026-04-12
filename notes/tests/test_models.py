import pytest
from .factories import NoteFactory, CategoryFactory, UserFactory
from ..models import Note, Category


@pytest.mark.django_db
def test_category_crud():
    category = CategoryFactory(title="Навчання")
    assert category.id is not None
    assert str(category) == "Навчання"

    category.title = "Університет"
    category.save()
    assert Category.objects.get(id=category.id).title == "Університет"

    category_id = category.id
    category.delete()
    assert not Category.objects.filter(id=category_id).exists()


@pytest.mark.django_db
def test_note_crud_and_links(user, category):
    note = NoteFactory(
        author=user,
        category=category,
        title="Здати дз по Django",
        text="Написати тести для CRUD"
    )
    assert note.id is not None

    assert note.get_absolute_url() == f"/{note.pk}/"
    assert note.author.username == user.username

    note.title = "Здати дз вчасно!"
    note.save()
    assert Note.objects.get(id=note.id).title == "Здати дз вчасно!"

    note_id = note.id
    note.delete()
    assert not Note.objects.filter(id=note_id).exists()


@pytest.mark.django_db
def test_note_cascade_delete_with_user(user, category):
    NoteFactory(author=user, category=category)
    user_id = user.id
    user.delete()
    assert Note.objects.filter(author_id=user_id).count() == 0