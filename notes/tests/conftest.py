import pytest
from .factories import UserFactory, CategoryFactory, NoteFactory

@pytest.fixture
def user():
    return UserFactory()

@pytest.fixture
def category():
    return CategoryFactory()

@pytest.fixture
def note(user, category):
    return NoteFactory(author=user, category=category)