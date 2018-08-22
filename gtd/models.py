from datetime import datetime

from django.db import models
from django.db.models.signals import post_save
from django.utils import timezone
from recurrence.fields import RecurrenceField
from silk.profiling.profiler import silk_profile

from api.users.models import User


class GtdUser(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    user = models.OneToOneField(User, related_name="gtd_user")

    bin = models.OneToOneField('Folder', related_name="bin_owner")
    collectbox = models.OneToOneField('Folder', related_name="collectbox_owner")
    actions = models.OneToOneField('Folder', related_name="actions_owner")
    waiting_for = models.OneToOneField(
        'Folder', related_name="waitingfor_owner")
    tickler = models.OneToOneField('Folder', related_name="tickler_owner")
    someday = models.OneToOneField('Folder', related_name="someday_owner")

    def __str__(self):
        return self.user.username


class Folder(models.Model):
    BIN = 0
    COLLECTBOX = 1
    ACTIONS = 2
    WAITING_FOR = 3
    TICKLER = 4
    SOMEDAY = 5
    SPECIAL_FOLDER_CHOICES = (
        (BIN, "Bin"),
        (COLLECTBOX, "Collectbox"),
        (ACTIONS, "Actions"),
        (WAITING_FOR, "Waiting For"),
        (TICKLER, "Tickler"),
        (SOMEDAY, "Someday")
    )

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    owner = models.ForeignKey(User)
    name = models.CharField(max_length=100)

    special_type = models.PositiveSmallIntegerField(choices=SPECIAL_FOLDER_CHOICES, null=True, blank=True)

    def __str__(self):
        return self.name


class Context(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    owner = models.ForeignKey(User)
    name = models.CharField(max_length=100)
    glyph = models.CharField(max_length=100)
    color = models.CharField(max_length=6, default="ffffff")

    def __str__(self):
        return self.name


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
    notes = models.TextField(default="", blank=True)
    status = models.IntegerField(choices=STATUS_CHOICES, default=STATUS_OPEN)

    folder = models.ForeignKey(Folder)
    context = models.ForeignKey(Context)

    priority = models.IntegerField(default=0)

    recurrence = RecurrenceField(null=True, blank=True)

    dependencies = models.ManyToManyField('self',
                                          symmetrical=False,
                                          related_name='depends_on',
                                          blank=True)

    def __str__(self):
        return self.short_description

    @silk_profile(name='Save Action')
    def save(self, *args, **kwargs):
        # If we have just been completed
        if (self.status > self.STATUS_OPEN and self.completed_at is None):
            # Make an ActionRecurrence object for this Action,
            # and reset it with new start_at/due_at
            if (self.recurrence is not None and len(self.recurrence.rrules) > 0 and self.start_at):
                # Possible to create recurrence without dtstart, then it recurs to same date
                if self.recurrence.dtstart is None:
                    self.recurrence.dtstart = datetime.combine(timezone.make_naive(self.due_at).date(),
                                                               datetime.min.time())

                action_recurrence = ActionRecurrence.objects.create(
                    action=self,
                    status=self.status,
                    start_at=self.start_at,
                    due_at=self.due_at
                )
                action_recurrence.save()
                recur_date = self.recurrence.after(timezone.make_naive(self.start_at), inc=False)

                if recur_date is not None:
                    self.start_at = timezone.make_aware(datetime.combine(recur_date, self.start_at.time()))
                    self.due_at = timezone.make_aware(
                        datetime.combine(recur_date, self.due_at.time())) if self.due_at else None
                    self.status = self.STATUS_OPEN
                else:
                    self.completed_at = timezone.now()
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


def create_user(sender, instance, created, **kwargs):
    if not created:
        return

    Context.objects.create(name="Agenda", owner=instance)
    Context.objects.create(name="Calls", owner=instance)
    Context.objects.create(name="Computer", owner=instance)
    Context.objects.create(name="Errand", owner=instance)
    Context.objects.create(name="Home", owner=instance)
    Context.objects.create(name="Office", owner=instance)
    Context.objects.create(name="Read/Review", owner=instance)
    Context.objects.create(name="Shopping", owner=instance)

    bin1 = Folder.objects.create(
        name="Bin", special_type=Folder.BIN, owner=instance)
    collectbox = Folder.objects.create(
        name="Collectbox", special_type=Folder.COLLECTBOX, owner=instance)
    actions = Folder.objects.create(
        name="Actions", special_type=Folder.ACTIONS, owner=instance)
    waiting_for = Folder.objects.create(
        name="Waiting For", special_type=Folder.WAITING_FOR, owner=instance)
    tickler = Folder.objects.create(
        name="Tickler", special_type=Folder.TICKLER, owner=instance)
    someday = Folder.objects.create(
        name="Someday", special_type=Folder.SOMEDAY, owner=instance)

    GtdUser.objects.create(
        user=instance, bin=bin1, collectbox=collectbox, actions=actions,
        waiting_for=waiting_for, tickler=tickler, someday=someday)


post_save.connect(create_user, sender=User,
                  dispatch_uid="gtd_create_user")
