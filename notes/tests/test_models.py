import pytest
from .factories import NoteFactory, UserFactory, CategoryFactory
from ..models import Note, Category


@pytest.mark.django_db
def test_category_creation():
    category = CategoryFactory(title="Терміново")

    assert category.id is not None
    assert category.title == "Терміново"
    assert str(category) == "Терміново"


@pytest.mark.django_db
def test_note_creation():
    note = NoteFactory(title="Тестова нотатка 1")

    assert note.id is not None
    assert note.title == "Тестова нотатка 1"
    assert note.category is not None


@pytest.mark.django_db
def test_note_update():
    note = NoteFactory(title="Стара назва нотатки")
    note.title = "Нова назва нотатки"
    note.save()

    assert Note.objects.get(id=note.id).title == "Нова назва нотатки"


@pytest.mark.django_db
def test_note_author_relationship():
    user = UserFactory(username="Ivan")
    note = NoteFactory(author=user)

    assert note.author.username == "Ivan"
    assert user.notes.count() == 1


@pytest.mark.django_db
def test_note_cascade_delete_with_user(user, category):
    NoteFactory(author=user, category=category, title="Секретна нотатка")

    assert Note.objects.filter(author=user).count() == 1

    user_id = user.id
    user.delete()
    assert Note.objects.filter(author_id=user_id).count() == 0