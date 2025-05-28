from django.urls import reverse
from django.utils.html import format_html
from django_tables2 import Table, tables

from .models import Hall, Employees, Exhibition, Excursion


class HallTable(Table):
    model = Hall
    attrs = {'class': 'paleblue'}
    actions = tables.Column(empty_values=(), verbose_name='Действия')

    def render_actions(self, record):
        edit_url = reverse('edit-hall', args=[record.pk])
        delete_url = reverse('delete-hall', args=[record.pk])
        return format_html(
            '<a href="{}" class="btn btn-sm btn-primary">Редактировать</a> '
            '<a href="{}" class="btn btn-sm btn-danger">Удалить</a>',
            edit_url,
            delete_url
        )

    class Meta:
        model = Hall
        template_name = "django_tables2/bootstrap5.html"
        fields = ("number", "title", "description", "level", "square", "actions")


class EmployeesTable(Table):
    model = Employees
    attrs = {'class': 'paleblue'}
    actions = tables.Column(empty_values=(), verbose_name='Действия')

    def render_actions(self, record):
        edit_url = reverse('edit-employee', args=[record.pk])
        delete_url = reverse('delete-employee', args=[record.pk])
        return format_html(
            '<a href="{}" class="btn btn-sm btn-primary">Редактировать</a> '
            '<a href="{}" class="btn btn-sm btn-danger">Удалить</a>',
            edit_url,
            delete_url
        )

    class Meta:
        model = Hall
        template_name = "django_tables2/bootstrap5.html"
        fields = ("full_name", "birth_date", "phone", "type", "hall", "hall__level", "actions")


class ExhibitionTable(Table):
    model = Exhibition
    attrs = {'class': 'paleblue'}
    actions = tables.Column(empty_values=(), verbose_name='Действия')

    def render_actions(self, record):
        edit_url = reverse('edit-exhibition', args=[record.pk])
        delete_url = reverse('delete-exhibition', args=[record.pk])
        return format_html(
            '<a href="{}" class="btn btn-sm btn-primary">Редактировать</a> '
            '<a href="{}" class="btn btn-sm btn-danger">Удалить</a>',
            edit_url,
            delete_url
        )

    class Meta:
        model = Exhibition
        template_name = "django_tables2/bootstrap5.html"
        fields = ("name", "date_from", "date_to", "exhibits")


class ExcursionTable(Table):
    model = Excursion
    attrs = {'class': 'paleblue'}
    actions = tables.Column(empty_values=(), verbose_name='Действия')

    def __init__(self, *args, user=None, **kwargs):
        if not (user and user.is_superuser):
            self.base_columns.pop('actions', None)
        super().__init__(*args, **kwargs)

    def render_actions(self, record, user):
        if user.is_superuser:
            edit_url = reverse('edit-excursion', args=[record.pk])
            delete_url = reverse('delete-excursion', args=[record.pk])
            return format_html(
            '<a href="{}" class="btn btn-sm btn-primary">Редактировать</a> '
            '<a href="{}" class="btn btn-sm btn-danger">Удалить</a>',
            edit_url,
            delete_url
        )

    class Meta:
        model = Exhibition
        template_name = "django_tables2/bootstrap5.html"
        fields = ("name", "exhibition", "employee")
