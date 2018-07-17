from django.utils import dateparse
from rest_framework import filters
from rest_framework.exceptions import ValidationError


class UpdatedSinceFilterBackend(filters.BaseFilterBackend):
    def filter_queryset(self, request, queryset, view):
        if 'updatedSince' not in request.query_params:
            return queryset.all()

        updated_since = dateparse.parse_datetime(request.query_params.get('updatedSince'))
        if updated_since is None:
            raise ValidationError("Could not parse updatedSince")

        return queryset.filter(updated_at__gt=updated_since)
