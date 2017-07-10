from datetime import datetime, time, timedelta

from django.test import TestCase
from django.utils import timezone

import recurrence

# Create your tests here.
from .models import Action, ActionRecurrence
from api.users.models import User

class QuestionModelTests(TestCase):

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

        print(pattern)

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


