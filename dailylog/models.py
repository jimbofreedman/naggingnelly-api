from django.db import models
from api.users.models import User


class DailyLog(models.Model):
    user = models.ForeignKey(User)
    date = models.DateField(auto_now_add=True)

    dream_diary = models.TextField(null=True, blank=True)
    chimp_management = models.TextField(null=True, blank=True)

    def __str__(self):
        return str(self.date)
