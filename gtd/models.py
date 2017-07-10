from django.db import models
from api.users.models import User

# Create your models here.
class Action(models.Model):
    STATUS_OPEN = 0
    STATUS_FAILED = 1
    STATUS_CANCELLED = 2
    STATUS_COMPLETED = 3
    STATUS_CHOICES = (
        (STATUS_OPEN, 'Open'),
        (STATUS_FAILED, 'Failed'),
        (STATUS_CANCELLED, 'Cancelled'),
        (STATUS_COMPLETED, 'Completed'),
    )

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    owner = models.ForeignKey(User)
    short_description = models.CharField(max_length=100)
    status = models.IntegerField(choices=STATUS_CHOICES, default=STATUS_OPEN)

    priority = models.IntegerField(default=0)
