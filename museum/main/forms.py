from datetime import date

from dateutil.relativedelta import relativedelta
from django import forms
from django.forms import ModelForm, TextInput, Textarea, DateInput, Select, CheckboxSelectMultiple, NumberInput
from django_filters.fields import ModelMultipleChoiceField

from .models import Hall, Exhibits, Employees, Exhibition, Excursion, EmployeeContacts, Reviews, Vacancy, FAQ, News, \
    PromoCodes


class HallForm(ModelForm):
    class Meta:
        model = Hall
        fields = ["number", "title", "description", "level", "square"]
        widgets = {
            "number": NumberInput(attrs={'placeholder': 'Введите номер'}),
            "title": TextInput(attrs={'placeholder': 'Введите название'}),
            "description": Textarea(attrs={'placeholder': 'Введите описание'}),
            "level": NumberInput(attrs={'placeholder': 'Введите этаж'}),
            "square": NumberInput(attrs={'step': '0.01', 'placeholder': 'Введите площадь, например, 120.5'}),
        }


class ExhibitForm(ModelForm):
    class Meta:
        model = Exhibits
        fields = ["name", "description", "period", "art_form", "employee", "image"]
        labels = {
            'name': 'Название экспоната',
            'description': 'Описание экспоната',
            'period': 'Дата поступления',
            'art_form': 'Вид искусства',
            'employee': 'Смотрящий'
        }
        widgets = {
            "name": TextInput(),
            "description": Textarea(),
            "period": DateInput(attrs={'type': 'date', 'max': date.today()}),
            "art_form": Select(),
            "employee": Select(),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['employee'].queryset = Employees.objects.filter(type__name="Смотрящий")


class EmployeeForm(forms.ModelForm):
    work_phone = forms.CharField(required=False, label='Рабочий телефон',
                                 widget=TextInput(attrs={'placeholder': '+375 (29) 000-00-00'}))
    email = forms.EmailField(required=False, label='Электронная почта')
    description = forms.CharField(required=False, label='Описание работы', widget=Textarea)
    image = forms.ImageField(required=False, label='Загрузите изображение сотрудника')
    is_visible = forms.BooleanField(required=False, initial=True, label='Отображать на вкладке "Контакты"')

    class Meta:
        model = Employees
        fields = ["full_name", "birth_date", "phone", "hall", "type", "work_phone", "email", "description", "image"]
        labels = {
            'hall': 'Выберите зал',
            'type': 'Выберите позицию',
            'phone': 'Личный телефон'
        }
        widgets = {
            "full_name": TextInput(attrs={'placeholder': 'Введите ФИО'}),
            "birth_date": DateInput(attrs={'type': 'date', 'max': date.today() - relativedelta(years=18),
                                           'min': date.today() - relativedelta(years=80)}),
            "phone": TextInput(attrs={'placeholder': '+375 (29) 000-00-00'}),
            "type": Select(),
            "hall": Select(),
        }

    def save(self, commit=True):
        employee = super().save(commit)
        contacts_data = {
            "work_phone": self.cleaned_data.get("work_phone"),
            "email": self.cleaned_data.get("email"),
            "description": self.cleaned_data.get("description"),
            "image": self.cleaned_data.get("image"),
            "is_visible": bool(self.cleaned_data.get("is_visible"))
        }
        EmployeeContacts.objects.update_or_create(employee=employee, defaults=contacts_data)
        return employee


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
            'name': 'Название экспозиции',
            'date_from': 'Дата с',
            'date_to': 'Дата по',
            'exhibits': 'Экспонаты, которые участвуют в экспозиции'
        }
        widgets = {
            "name": TextInput(),
            "date_from": DateInput(attrs={'type': 'date'}),
            "date_to": DateInput(attrs={'type': 'date'}),
        }


class PromoCodesForm(forms.ModelForm):
    class Meta:
        model = PromoCodes
        fields = ['text']
        widgets = {
            'text': forms.Textarea(attrs={
                'rows': 3,
                'placeholder': 'Введите текст промокода',
                'class': 'dark-textarea'
            }),
            # 'status': forms.Select(attrs={'class': 'dark-select'})
        }


class ExcursionForm(ModelForm):
    class Meta:
        model = Excursion
        fields = ["name", "exhibition", "employee"]
        labels = {
            'name': 'Название экскурсии',
            'exhibition': 'Выберите экспозицию',
            'employee': 'Выберите экскурсовода'
        }
        widgets = {
            "name": TextInput(),
            "exhibition": Select(),
            "employee": Select()
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['employee'].queryset = Employees.objects.filter(type__name="Экскурсовод")


class NewsForm(ModelForm):
    class Meta:
        model = News
        fields = ["name", "summary", "description", "image"]
        labels = {
            'name': 'Введите название новости',
            'summary': 'Введите краткое содержание новости',
            'description': 'Введите описание новости',
            'image': 'Загрузите изображение'
        }

    widgets = {
        "name": TextInput(attrs={
            'class': 'form-control'}),
        "summary": TextInput(attrs={
            'class': 'form-control'}),
        "description": Textarea(attrs={
            'class': 'form-control',
        }),
    }


class FAQForm(ModelForm):
    class Meta:
        model = FAQ
        fields = ["question", "answer"]
        labels = {
            'question': 'Введите вопрос',
            'answer': 'Введите ответ'
        }

    widgets = {
        "question": TextInput(attrs={
            'class': 'form-control'}),
        "answer": TextInput(attrs={
            'class': 'form-control'}),
    }


class VacancyForm(ModelForm):
    class Meta:
        model = Vacancy
        fields = ["name", "description", "salary"]

    widgets = {
        "name": TextInput(attrs={
            'class': 'form-control'
        }),
        "description": Textarea(attrs={
            'class': 'form-control',
        }),
        "salary": NumberInput(attrs={
            'class': 'form-control',
        })
    }


class ReviewForm(ModelForm):
    class Meta:
        model = Reviews
        fields = ["grade", "text"]
        widgets = {
            "grade": forms.HiddenInput(),
            "text": forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 4,
                'placeholder': 'Поделитесь вашим впечатлением...',
            }),
        }
