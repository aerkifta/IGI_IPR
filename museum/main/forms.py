from datetime import date

from dateutil.relativedelta import relativedelta
from django.forms import ModelForm, TextInput, Textarea, DateInput, Select, CheckboxSelectMultiple
from django_filters.fields import ModelMultipleChoiceField

from .models import Hall, Exhibits, Employees, Exhibition, Excursion


class HallForm(ModelForm):
    class Meta:
        model = Hall
        fields = ["number", "title", "description", "level", "square"]
        widgets = {
            "number": TextInput(attrs={
                'type': 'number',
                'class': 'form-control',
                'placeholder': 'Введите номер'}),
            "title": TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Введите название'}),
            "description": Textarea(attrs={
                'class': 'form-control',
                'placeholder': 'Введите описание',
            }),
            "level": TextInput(attrs={
                'type': 'number',
                'class': 'form-control',
                'placeholder': 'Введите этаж'}),
            "square": TextInput(attrs={
                'type': 'number',
                'class': 'form-control',
                'step': '0.01',
                'placeholder': 'Введите площадь, например, 120.5'}),
        }


class ExhibitForm(ModelForm):
    class Meta:
        model = Exhibits
        fields = ["name", "description", "period", "art_form", "employee", "image"]
        labels = {
            'name': 'Введите название экспоната',
            'description': 'Введите описание экспоната',
            'period': 'Введите дату поступления экспоната',
            'art_form': 'Выберите вид искусства, к которому относится экспонат ',
            'employee': 'Выберите смотрящего '
        }
        widgets = {
            "name": TextInput(attrs={
                'class': 'form-control'}),
            "description": Textarea(attrs={
                'class': 'form-control',
            }),
            "period": DateInput(attrs={
                'type': 'date',
                'class': 'form-control',
                'max': date.today()
            }),
            "art_form": Select(attrs={
                'class': 'form-select'
            }),
            "employee": Select(attrs={
                'class': 'form-select'
            }),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['employee'].queryset = Employees.objects.filter(type__name="Смотрящий")


class EmployeeForm(ModelForm):
    class Meta:
        model = Employees
        fields = ["full_name", "birth_date", "phone", "hall", "type"]
        widgets = {
            "full_name": TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Введите ФИО'}),
            "birth_date": DateInput(attrs={
                'type': 'date',
                'class': 'form-control',
                'max': date.today() - relativedelta(years=18),
                'min': date.today() - relativedelta(years=80),
            }),
            "phone": TextInput(attrs={
                'type': 'text',
                'class': 'form-control',
                'id': 'phone',
                'name': 'phone',
                'placeholder': '+375 (29) 000-00-00'}),
            "type": Select(attrs={
                'class': 'form-select'
            }),
            "hall": Select(attrs={
                'class': 'form-select'
            }),
        }


class ExhibitionForm(ModelForm):
    exhibits = ModelMultipleChoiceField(
        queryset=Exhibits.objects.all(),
        widget=CheckboxSelectMultiple,
        required=False,
        label='Выберите экспонаты'
    )

    class Meta:
        model = Exhibition
        fields = ["name", "date_from", "date_to", "exhibits"]
        labels = {
            'name': 'Введите название экспозиции',
            'date_from': 'Введите дату с',
            'date_to': 'Введите дату по',
            'exhibits': 'Выберите экспонаты, которые учавствуют в экспозиции '
        }
        widgets = {
            "name": TextInput(attrs={
                'class': 'form-control'}),
            "description": Textarea(attrs={
                'class': 'form-control',
            }),
            "date_from": DateInput(attrs={
                'type': 'date',
                'class': 'form-control'
            }),
            "date_to": DateInput(attrs={
                'type': 'date',
                'class': 'form-control'
            }),
            "exhibits": CheckboxSelectMultiple(attrs={
                'class': 'form-control'
            })
        }


class ExcursionForm(ModelForm):
    class Meta:
        model = Excursion
        fields = ["name", "exhibition", "employee"]
        labels = {
            'name': 'Введите название экспозиции',
            'exhibition': 'Выберите экспозицию',
            'employee': 'Выберите экскурсовода'
        }
        widgets = {
            "name": TextInput(attrs={
                'class': 'form-control'}),
            "exhibition": Select(attrs={
                'class': 'form-control'
            }),
            "employee": Select(attrs={
                'class': 'form-control'
            })
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['employee'].queryset = Employees.objects.filter(type__name="Экскурсовод")
