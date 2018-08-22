from django.test import TestCase
from faker import Faker
from gtd.models import Folder

from api.users.models import User


class FolderModelTests(TestCase):
    def setUp(self):
        self.faker = Faker()
        self.user = User.objects.create(username=self.faker.name())

    def test_str(self):
        name = self.faker.name()
        folder = Folder.objects.create(
            owner=self.user,
            name=name,
        )
        self.assertEqual(str(folder), name)
