import json

from badthing.models import BadThing, BadThingType
from django.core.urlresolvers import reverse
from faker import Faker
from rest_framework import status
from rest_framework.test import APIRequestFactory, APITestCase, force_authenticate

from api.users.models import User


class BadThingTypeTest(APITestCase):
    def setUp(self):
        self.faker = Faker()
        self.username = self.faker.name()
        self.password = self.faker.name()
        self.user = User.objects.create_user(username=self.username, password=self.password)
        self.other_user = User.objects.create_user(username=self.faker.name(), password=self.faker.name())

    def test_list(self):
        self.client.login(username=self.username, password=self.password)
        name1 = self.faker.name()
        name2 = self.faker.name()
        type1 = BadThingType.objects.create(name=name1, owner=self.user)
        type2 = BadThingType.objects.create(name=name2, owner=self.user)
        BadThingType.objects.create(name=self.faker.name(), owner=self.other_user)

        response = self.client.get("/badthing/bad_thing_types/")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertJSONEqual(response.content, [
            {"id": type1.id, "name": name1},
            {"id": type2.id, "name": name2}
        ])

    def test_list_logged_out(self):
        response = self.client.get("/badthing/bad_thing_types/")
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_detail(self):
        self.client.login(username=self.username, password=self.password)
        name = self.faker.name()
        type = BadThingType.objects.create(name=name, owner=self.user)

        response = self.client.get("/badthing/bad_thing_types/{}/".format(type.id))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertJSONEqual(response.content, {"id": type.id, "name": name})

    def test_get_logged_out(self):
        name = self.faker.name()
        type = BadThingType.objects.create(name=name, owner=self.user)
        response = self.client.get("/badthing/bad_thing_types/{}/".format(type.id))
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_get_wrong_user(self):
        self.client.login(username=self.username, password=self.password)
        name = self.faker.name()
        type = BadThingType.objects.create(name=name, owner=self.other_user)
        response = self.client.get("/badthing/bad_thing_types/{}/".format(type.id))
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_create(self):
        self.client.login(username=self.username, password=self.password)
        name = self.faker.name()
        response = self.client.post("/badthing/bad_thing_types/", {"name": name})
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(json.loads(response.content)["name"], name)

    def test_create_logged_out(self):
        response = self.client.post("/badthing/bad_thing_types/", {"name": self.faker.name()})
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
