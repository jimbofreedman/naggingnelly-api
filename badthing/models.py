from django.db import models
from api.users.models import User

# Create your models here.
class BadThingType(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    owner = models.ForeignKey(User)

    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name

class BadThing(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    owner = models.ForeignKey(User)

    type = models.ForeignKey(BadThingType)

    def __str__(self):
        return self.type.name
