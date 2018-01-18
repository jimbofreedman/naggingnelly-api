import json

from badthing.models import BadThing, BadThingType
from django.core.urlresolvers import reverse
from faker import Faker
from rest_framework import status
from rest_framework.test import APIRequestFactory, APITestCase, force_authenticate

from api.users.models import User


class BadThingTest(APITestCase):
    def setUp(self):
        self.faker = Faker()
        self.username = self.faker.name()
        self.password = self.faker.name()
        self.user = User.objects.create_user(username=self.username, password=self.password)
        self.type1 = BadThingType.objects.create(name=self.faker.name(), owner=self.user)
        self.type2 = BadThingType.objects.create(name=self.faker.name(), owner=self.user)
        self.other_user = User.objects.create_user(username=self.faker.name(), password=self.faker.name())
        self.other_user_type = BadThingType.objects.create(name=self.faker.name(), owner=self.other_user)

    def test_list(self):
        self.client.login(username=self.username, password=self.password)
        thing1 = BadThing.objects.create(type=self.type1, owner=self.user)
        thing2 = BadThing.objects.create(type=self.type2, owner=self.user)
        BadThingType.objects.create(name=self.faker.name(), owner=self.other_user)

        response = self.client.get("/badthing/bad_things/")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertJSONEqual(response.content, [
            {"id": thing1.id, "type": self.type1.id},
            {"id": thing2.id, "type": self.type2.id}
        ])

    def test_list_logged_out(self):
        response = self.client.get("/badthing/bad_things/")
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_detail(self):
        self.client.login(username=self.username, password=self.password)
        thing = BadThing.objects.create(type=self.type1, owner=self.user)

        response = self.client.get("/badthing/bad_things/{}/".format(thing.id))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertJSONEqual(response.content, {"id": thing.id, "type": self.type1.id})

    def test_get_logged_out(self):
        thing = BadThing.objects.create(type=self.type1, owner=self.user)

        response = self.client.get("/badthing/bad_things/{}/".format(thing.id))
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_get_wrong_user(self):
        self.client.login(username=self.username, password=self.password)
        thing = BadThing.objects.create(type=self.other_user_type, owner=self.other_user)

        response = self.client.get("/badthing/bad_things/{}/".format(thing.id))
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_create(self):
        self.client.login(username=self.username, password=self.password)
        response = self.client.post("/badthing/bad_things/", {"type": self.type1.id})
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(json.loads(response.content)["type"], self.type1.id)

    def test_create_logged_out(self):
        response = self.client.post("/badthing/bad_things/", {"type": self.type1.id})
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_create_other_user_type(self):
        self.client.login(username=self.username, password=self.password)
        response = self.client.post("/badthing/bad_things/", {"type": self.other_user_type.id})
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
