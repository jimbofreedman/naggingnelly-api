from datetime import datetime, date, timedelta
from recurrence.fields import RecurrenceField
from django.db import models
from django.utils import timezone
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
    completed_at = models.DateTimeField(null=True, blank=True)

    start_at = models.DateTimeField(null=True, blank=True)
    due_at = models.DateTimeField(null=True, blank=True)

    owner = models.ForeignKey(User)
    short_description = models.CharField(max_length=100)
    status = models.IntegerField(choices=STATUS_CHOICES, default=STATUS_OPEN)

    priority = models.IntegerField(default=0)

    recurrence = RecurrenceField(null=True, blank=True)

    dependencies = models.ManyToManyField('self',
                                           symmetrical=False,
                                           related_name='depends_on',
                                           blank=True)


    def __str__(self):
        return self.short_description

    def save(self, *args, **kwargs):
        # If we have just been completed
        if (self.status > self.STATUS_OPEN and self.completed_at is None):
            # Make an ActionRecurrence object for this Action,
            # and reset it with new start_at/due_at
            if (self.recurrence is not None and len(self.recurrence.rrules) > 0 and self.start_at):
                action_recurrence = ActionRecurrence.objects.create(
                    action=self,
                    status=self.status,
                    start_at=self.start_at,
                    due_at=self.due_at
                )
                action_recurrence.save()
                recur_date = self.recurrence.after(timezone.make_naive(self.start_at), inc=False)
                self.start_at = timezone.make_aware(datetime.combine(recur_date, self.start_at.time()))
                self.due_at = timezone.make_aware(datetime.combine(recur_date, self.due_at.time())) if self.due_at else None
                self.status = self.STATUS_OPEN
            else:
                self.completed_at = timezone.now()

        is_new = self.id is None

        super(Action, self).save(*args, **kwargs)

        if is_new and self.priority == 0:
            self.priority = self.id * 10000
            super(Action, self).save()

class ActionRecurrence(models.Model):
    action = models.ForeignKey(Action)
    status = models.IntegerField(choices=Action.STATUS_CHOICES)

    start_at = models.DateTimeField(null=True, blank=True)
    due_at = models.DateTimeField(null=True, blank=True)
    completed_at = models.DateTimeField(auto_now_add=True)
