from django.forms import TextInput
from django_filters import FilterSet, CharFilter

from .models import Hall, Employees, Exhibition, Excursion


class HallFilter(FilterSet):
    title = CharFilter(
        lookup_expr='icontains',
        label='Поиск по названию',
        widget=TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Введите название',
            'style': 'width: 300px;'
        }))
    description = CharFilter(
        lookup_expr='icontains',
        label='Поиск по описанию',
        widget=TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Введите описание',
            'style': 'width: 300px;'
        })
    )

    class Meta:
        model = Hall
        fields = ['title', 'description']


class EmployeeFilter(FilterSet):
    full_name = CharFilter(
        lookup_expr='icontains',
        label='Поиск по ФИО',
        widget=TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Введите ФИО',
            'style': 'width: 300px;'
        }))
    hall__level = CharFilter(
        field_name='hall__level',
        lookup_expr='exact',
        label='Этаж',
        widget=TextInput(attrs={
            'type':'number',
            'class': 'form-control',
            'placeholder': 'Введите этаж',
            'style': 'width: 150px;'
        })
    )

    class Meta:
        model = Employees
        fields = ['full_name','hall__level']

class ExhibitionFilter(FilterSet):
    name = CharFilter(
        lookup_expr='icontains',
        label='Поиск по наименованию',
        widget=TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Введите наименование',
            'style': 'width: 300px;'
        }))

    class Meta:
        model = Exhibition
        fields = ['name']

class ExcursionFilter(FilterSet):
    name = CharFilter(
        lookup_expr='icontains',
        label='Поиск по наименованию',
        widget=TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Введите наименование',
            'style': 'width: 300px;'
        }))

    class Meta:
        model = Excursion
        fields = ['name']
