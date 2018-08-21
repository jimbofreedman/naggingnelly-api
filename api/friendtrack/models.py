from django.db import models
from api.users.models import User

class Category(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    owner = models.ForeignKey(User)

    name = models.CharField(max_length=50)
    order = models.SmallIntegerField(default=0)

    class Meta:
        ordering = ('order', 'name', )


class Friend(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    owner = models.ForeignKey(User)

    facebook_name = models.CharField(max_length=200, null=True, blank=True)
    override_name = models.CharField(max_length=200, null=True, blank=True)
    added_at = models.DateField(null=True, blank=True)

    category = models.ForeignKey(Category)

    @property
    def name(self):
        return self.override_name or self.facebook_name

    def __str__(self):
        return self.name

    class Meta:
        ordering = ('override_name', 'facebook_name', )

