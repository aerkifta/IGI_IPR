from django.contrib.auth.models import User
from django.db import models


class Hall(models.Model):
    id = models.IntegerField(primary_key=True)
    number = models.IntegerField('Номер')
    title = models.CharField('Зал', max_length=100)
    description = models.TextField('Описание')
    level = models.SmallIntegerField('Этаж')
    square = models.FloatField('Площадь')

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = 'Зал'
        verbose_name_plural = 'Залы'


class ArtForm(models.Model):
    name = models.CharField('Наименование', max_length=100)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Вид искусства'
        verbose_name_plural = 'Виды искусства'


class TypeEmployee(models.Model):
    name = models.CharField("Наименование должности", max_length=100)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Должность'
        verbose_name_plural = 'Должности'


class Employees(models.Model):
    full_name = models.CharField("ФИО", max_length=100)
    birth_date = models.DateField("День рождения")
    phone = models.TextField("Телефон", max_length=30)
    type = models.ForeignKey(TypeEmployee, on_delete=models.CASCADE, null=True, blank=True, default=None)
    hall = models.ForeignKey(Hall, on_delete=models.CASCADE, null=True, blank=True, default=None)

    def __str__(self):
        return self.full_name

    class Meta:
        verbose_name = 'Работник'
        verbose_name_plural = 'Работники'


class Exhibits(models.Model):
    name = models.CharField('Наименование', max_length=100)
    description = models.TextField('Описание')
    period = models.DateField('Дата поступления')
    image = models.ImageField(upload_to='exhibits/', null=True, blank=True)
    art_form = models.ForeignKey(ArtForm, on_delete=models.CASCADE, null=True, blank=True, default=None)
    employee = models.ForeignKey(Employees, on_delete=models.CASCADE, null=True, blank=True, default=None)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Экспонат'
        verbose_name_plural = 'Экспонаты'


class Exhibition(models.Model):
    name = models.CharField('Наименование', max_length=100)
    date_from = models.DateField('Дата с')
    date_to = models.DateField('Дата по')
    exhibits = models.ManyToManyField(Exhibits)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Экспозиция'
        verbose_name_plural = 'Экспозиции'


class Exposition(models.Model):
    exhibit = models.ForeignKey(Exhibits, on_delete=models.CASCADE, null=True, blank=True, default=None)
    exhibition = models.ForeignKey(Exhibition, on_delete=models.CASCADE, null=True, blank=True, default=None)

class Excursion(models.Model):
    name = models.CharField('Наименование', max_length=100)
    exhibition = models.OneToOneField(Exhibition, on_delete=models.CASCADE, null=True, blank=True, default=None)
    employee =  models.ForeignKey(Employees, on_delete=models.CASCADE, null=True, blank=True, default=None)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Экскурсия'
        verbose_name_plural = 'Экскурсии'
