from django_filters import FilterSet, DateTimeFilter
from django.forms import DateTimeInput

from .models import *


class AdFilter(FilterSet):
    added_after = DateTimeFilter(
        field_name='time_add',
        lookup_expr='gt',
        widget=DateTimeInput(
            format='%Y-%m-%dT%H:%M',
            attrs={'type': 'datetime-local'},
            ),
        label='Add after'
    )

    class Meta:
        model = Advert
        fields = {
            'author__username': ['icontains'],
            'title': ['icontains'],
            'category': ['exact'],

        }

