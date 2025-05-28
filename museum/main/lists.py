from django_filters.views import FilterView
from django_tables2 import SingleTableMixin

from .filters import HallFilter
from .models import Hall
from .tables import HallTable


class HallList(SingleTableMixin, FilterView):
    model = Hall
    table_class = HallTable
    template_name = "main/halls.html"
    filterset_class = HallFilter
    paginate_by = 5

    def get_paginate_by(self, queryset):
        per_page = self.request.GET.get("per_page")
        if per_page and per_page.isdigit():
            return int(per_page)
        return 5
