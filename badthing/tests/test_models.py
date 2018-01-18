from django.test import TestCase
from faker import Faker

from api.users.models import User

from ..models import BadThing, BadThingType


class BadThingTypeTest(TestCase):
    def setUp(self):
        self.faker = Faker()
        self.username = self.faker.name()
        self.user = User.objects.create(username=self.username)

    def test_str(self):
        name = self.faker.name()
        bad_thing_type = BadThingType.objects.create(name=name, owner=self.user)
        self.assertEqual(str(bad_thing_type), name)


class BadThingTest(TestCase):
    def setUp(self):
        self.faker = Faker()
        self.username = self.faker.name()
        self.user = User.objects.create(username=self.username)
        self.bad_thing_type_name = self.faker.name()
        self.bad_thing_type = BadThingType.objects.create(name=self.bad_thing_type_name, owner=self.user)

    def test_str(self):
        bad_thing = BadThing.objects.create(type=self.bad_thing_type, owner=self.user)
        self.assertEqual(str(bad_thing), self.bad_thing_type_name)
