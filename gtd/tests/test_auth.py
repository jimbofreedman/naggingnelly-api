from django.test import TransactionTestCase
from django.urls import reverse
from faker import Faker
from rest_framework import status
from rest_framework.authtoken.models import Token
from rest_framework.test import RequestsClient

from api.users.models import User


class ApiAuthTests(TransactionTestCase):
    def setUp(self):
        self.faker = Faker()
        self.user = User.objects.create(username="asdf@asdf.com", email="asdf@asdf.com")
        self.user.set_password("asdfasdf")
        self.user.save()
        self.token = Token.objects.create(user=self.user)
        self.body = {"authentication_token": self.token.key,
                     "shortDescription": "hi",
                     "folder": self.user.folder_set.first().id,
                     "context": self.user.context_set.first().id
                     }
        self.client = RequestsClient()
        self.client.headers.update({'x-test': 'true'})

    def get_url(self, name, args=None):
        return 'https://testserver' + reverse(name, args=args)

    def test_token_header(self):
        self.client.headers.update({'Authorization': 'Token {}'.format(self.token.key)})
        response = self.client.post(self.get_url('gtd:actions-list'), json=self.body)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_token_body(self):
        response = self.client.post(self.get_url('gtd:actions-list'), json=self.body)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_login(self):
        response = self.client.post(self.get_url('rest_login'), json={"email": "asdf@asdf.com", "password": "asdfasdf"})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
