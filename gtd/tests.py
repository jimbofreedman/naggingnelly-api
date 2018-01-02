from datetime import datetime, time, timedelta

from django.test import TestCase
from django.utils import timezone
from freezegun import freeze_time

import recurrence

# Create your tests here.
from .models import Action, ActionRecurrence
from api.users.models import User

class ActionModelTests(TestCase):

    def test_new_task_priority(self):
        user = User.objects.create(
                email="blah@blah.com"
        )

        action = Action.objects.create(
            owner=user,
            short_description="Test Action"
        )

        action.save()
        self.assertEqual(action.priority, action.id * 10000)


    def test_new_task_specified_priority(self):
        user = User.objects.create(
            email="blah@blah.com"
        )

        action = Action.objects.create(
            owner=user,
            short_description="Test Action",
            priority=-10
        )

        action.save()
        self.assertEqual(action.priority, -10)

    def test_complete_task_no_recurrence(self):
        user = User.objects.create(
            email="blah@blah.com"
        )

        action = Action.objects.create(
            owner=user,
            short_description="Test Action"
        )

        action.save()
        self.assertIs(action.status, action.STATUS_OPEN)
        action.status = action.STATUS_COMPLETED
        action.save()
        self.assertIs(action.status, action.STATUS_COMPLETED)


    @freeze_time("2017-01-01 10:00:00")
    def test_complete_task_daily_recurrence(self):
        myrule = recurrence.Rule(
            recurrence.DAILY
        )

        pattern = recurrence.Recurrence(
            dtstart=datetime(2014, 1, 2, 0, 0, 0),
            dtend=datetime(2150, 1, 3, 0, 0, 0),
            rrules=[myrule, ]
        )

        user = User.objects.create(
            email="blah@blah.com"
        )

        start_at = timezone.make_aware(datetime(2017, 1, 1, 7, 0, 0))
        due_at = timezone.make_aware(datetime(2017, 1, 1, 10, 0, 0))

        next_start_at = timezone.make_aware(datetime.combine(datetime.today() + timedelta(days=1), time(7, 0)))
        next_due_at = timezone.make_aware(datetime.combine(datetime.today() + timedelta(days=1), time(10, 0)))

        action = Action.objects.create(
            owner=user,
            short_description="Test Action",
            recurrence=pattern,
            start_at=start_at,
            due_at=due_at
        )
        action.save()
        self.assertIs(action.status, action.STATUS_OPEN)
        action.status = action.STATUS_COMPLETED
        action.save()
        self.assertIs(action.status, action.STATUS_OPEN)
        action_recurrence = ActionRecurrence.objects.get(pk=1)
        self.assertIs(action_recurrence.action.id, action.id)
        self.assertIs(action_recurrence.status, action.STATUS_COMPLETED)
        self.assertEqual(action_recurrence.start_at, start_at)
        self.assertEqual(action_recurrence.due_at, due_at)
        self.assertEqual(action.start_at, next_start_at)
        self.assertEqual(action.due_at, next_due_at)
        self.assertEqual(action.completed_at, None)

    @freeze_time("2017-08-02 22:17:51")
    def test_complete_task_weekly_recurrence(self):
        myrule = recurrence.Rule(
            recurrence.WEEKLY, byday=[recurrence.base.WE]
        )

        pattern = recurrence.Recurrence(
            #dtstart=datetime(2014, 1, 2, 0, 0, 0),
            #dtend=datetime(2150, 1, 3, 0, 0, 0),
            rrules=[myrule, ]
        )

        user = User.objects.create(
            email="blah@blah.com"
        )

        start_at = timezone.make_aware(datetime(2017, 8, 2, 8, 0, 0))
        due_at = timezone.make_aware(datetime(2017, 8, 2, 13, 0, 0))

        next_start_at = start_at + timedelta(days=7)
        next_due_at = due_at + timedelta(days=7)

        action = Action.objects.create(
            owner=user,
            short_description="Test Action",
            recurrence=pattern,
            start_at=start_at,
            due_at=due_at
        )
        action.save()
        self.assertIs(action.status, action.STATUS_OPEN)
        action.status = action.STATUS_COMPLETED
        action.save()
        self.assertIs(action.status, action.STATUS_OPEN)
        action_recurrence = ActionRecurrence.objects.get(action=action)
        self.assertIs(action_recurrence.action.id, action.id)
        self.assertIs(action_recurrence.status, action.STATUS_COMPLETED)
        self.assertEqual(action_recurrence.start_at, start_at)
        self.assertEqual(action_recurrence.due_at, due_at)

        new_action = Action.objects.get(pk=action.id)
        self.assertEqual(new_action.start_at, next_start_at)
        self.assertEqual(new_action.due_at, next_due_at)
        self.assertEqual(new_action.completed_at, None)

    @freeze_time("2017-01-02 10:00:00")
    def test_complete_task_monthly_recurrence(self):
        myrule = recurrence.Rule(
            recurrence.MONTHLY, bymonthday=[1]
        )

        pattern = recurrence.Recurrence(
            dtstart=datetime(2014, 1, 2, 0, 0, 0),
            dtend=datetime(2150, 1, 3, 0, 0, 0),
            rrules=[myrule, ]
        )

        user = User.objects.create(
            email="blah@blah.com"
        )

        start_at = timezone.make_aware(datetime(2017, 1, 1, 7, 0, 0))
        due_at = timezone.make_aware(datetime(2017, 1, 1, 10, 0, 0))

        next_start_at = start_at + timedelta(days=31)
        next_due_at = due_at + timedelta(days=31)

        action = Action.objects.create(
            owner=user,
            short_description="Test Action",
            recurrence=pattern,
            start_at=start_at,
            due_at=due_at
        )
        action.save()
        self.assertIs(action.status, action.STATUS_OPEN)
        action.status = action.STATUS_COMPLETED
        action.save()
        self.assertIs(action.status, action.STATUS_OPEN)
        action_recurrence = ActionRecurrence.objects.get(action=action)
        self.assertIs(action_recurrence.action.id, action.id)
        self.assertIs(action_recurrence.status, action.STATUS_COMPLETED)
        self.assertEqual(action_recurrence.start_at, start_at)
        self.assertEqual(action_recurrence.due_at, due_at)
        self.assertEqual(action.start_at, next_start_at)
        self.assertEqual(action.due_at, next_due_at)
        self.assertEqual(action.completed_at, None)



