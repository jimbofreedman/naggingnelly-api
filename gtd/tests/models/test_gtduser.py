from datetime import datetime, time, timedelta

import recurrence
from django.test import TestCase
from django.utils import timezone
from faker import Faker
from freezegun import freeze_time
from gtd.models import GtdUser

from api.users.models import User


class FolderModelTests(TestCase):
    def setUp(self):
        self.faker = Faker()

    def test_str(self):
        name = self.faker.name()
        user = User.objects.create(username=name)
        gtd_user = GtdUser.objects.get(user=user)
        self.assertEqual(str(gtd_user), name)
