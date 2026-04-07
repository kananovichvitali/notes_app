import factory
from django.contrib.auth.models import User
from ..models import Note, Category

class UserFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = User
    username = factory.Faker('user_name')


class CategoryFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Category
    title = factory.Faker('word')


class NoteFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Note

    title = factory.Faker('sentence', nb_words=4)
    text = factory.Faker('paragraph')
    category = factory.SubFactory(CategoryFactory)
    author = factory.SubFactory(UserFactory)