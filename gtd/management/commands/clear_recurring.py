from django.core.management.base import BaseCommand
from django.utils import timezone

from .models import Action


class Command(BaseCommand):
    def handle(self, *args, **options):
        while True:
            actions = Action.objects.filter(recurrence__isnull=False,
                                            status=Action.STATUS_OPEN,
                                            due_at__lte=timezone.now())

            if actions.count() == 0:
                return

            for a in actions:
                a.status = Action.STATUS_FAILED
                a.save()
