from django.test import TestCase

from faker import Faker

from api.users.models import User

from ...models import GtdUser


class FolderModelTests(TestCase):
    def setUp(self):
        self.faker = Faker()

    def test_str(self):
        name = self.faker.name()
        user = User.objects.create(username=name)
        gtd_user = GtdUser.objects.get(user=user)
        self.assertEqual(str(gtd_user), name)
