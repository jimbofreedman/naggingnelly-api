from django.utils import dateparse
from rest_framework import filters
from rest_framework.exceptions import ValidationError


class UpdatedSinceFilterBackend(filters.BaseFilterBackend):
    def filter_queryset(self, request, queryset, view):
        if 'updated_since' not in request.query_params:
            return queryset.all()

        updated_since = dateparse.parse_datetime(request.query_params.get('updated_since'))
        if updated_since is None:
            raise ValidationError("Could not parse updated_since")

        return queryset.filter(updated_at__gt=updated_since)
