from datetime import datetime, time, timedelta

import recurrence
from django.test import TestCase
from django.utils import timezone
from faker import Faker
from freezegun import freeze_time
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
