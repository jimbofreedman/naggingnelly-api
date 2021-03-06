import re
import sys

from django.core.management.base import BaseCommand

from api.users.models import User

from .models import Action


class Command(BaseCommand):
    def _find_or_add(self, desc):
        user = User.objects.get(pk=1)
        actions = Action.objects.filter(short_description=desc)

        if (actions.count() > 0):
            return actions[0]
        else:
            return Action.objects.create(owner=user,
                                         short_description=desc)

    def handle(self, *args, **options):
        with options.get('stdin', sys.stdin) as f:
            graph = f.read()

        for match in re.findall("(\w*) -> (\w*);", graph):
            first = self._find_or_add(match[0])
            second = self._find_or_add(match[1])

            second.dependencies.add(first)
            second.save()
