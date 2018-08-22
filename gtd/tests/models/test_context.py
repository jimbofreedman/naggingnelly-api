from django.test import TestCase

from faker import Faker

from api.users.models import User

from ...models import Context


class ContextModelTests(TestCase):
    def setUp(self):
        self.faker = Faker()
        self.user = User.objects.create(username=self.faker.name())

    def test_str(self):
        name = self.faker.name()
        context = Context.objects.create(
            owner=self.user,
            name=name,
        )
        self.assertEqual(str(context), name)
