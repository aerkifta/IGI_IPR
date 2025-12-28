from django.contrib.auth.models import User
from django.core.validators import MinValueValidator, MaxValueValidator
from django.db import models
from django.db.models.fields import TextField, PositiveIntegerField
from django.utils.translation import gettext_lazy as _


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
    employee = models.ForeignKey(Employees, on_delete=models.CASCADE, null=True, blank=True, default=None)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Экскурсия'
        verbose_name_plural = 'Экскурсии'


class News(models.Model):
    name = models.CharField('Наименование', max_length=100)
    summary = models.CharField('Краткое содержание', max_length=200)
    description = models.TextField('Описание')
    image = models.ImageField(upload_to='news/', null=True, blank=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Новости'
        verbose_name_plural = 'Новости'


class FAQ(models.Model):
    question = models.CharField('Вопрос', max_length=100)
    answer = models.CharField('Ответ', max_length=100)

    def __str__(self):
        return self.question + self.answer

    class Meta:
        verbose_name = 'FAQ'
        verbose_name_plural = 'FAQ'


class EmployeeContacts(models.Model):
    employee = models.OneToOneField(Employees, on_delete=models.CASCADE, null=True, blank=True, default=None)
    work_phone = models.CharField('Рабочий телефон', max_length=100)
    email = models.CharField('E-mail', max_length=100)
    description = models.TextField('Описание выполняемых работ')
    image = models.ImageField(upload_to='employee_contacts/', null=True, blank=True)
    is_visible = models.BooleanField('Видимый', default=True)

    def __str__(self):
        return self.work_phone + ' ' + self.email

    class Meta:
        verbose_name = 'Контакты'
        verbose_name_plural = 'Контакты'


class Vacancy(models.Model):
    name = models.CharField('Наименование вакансии', max_length=100)
    description = models.TextField('Описание вакансии')
    salary = models.IntegerField('Зарплата')
    response_count = models.IntegerField('Количество откликов', default=0)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Вакансии'
        verbose_name_plural = 'Вакансии'


class Reviews(models.Model):
    grade = PositiveIntegerField('Оценка', default=0, validators=[MinValueValidator(0), MaxValueValidator(5)])
    text = TextField('Текст отзыва')
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.text

    class Meta:
        verbose_name = 'Отзывы'
        verbose_name_plural = 'Отзывы'

class PromoCodes(models.Model):
    class PromoStatus(models.TextChoices):
        ACTIVE = 'T', _('Active')
        ARCHIVED = 'A', _('Archived')
        DELETED = 'D', _('Deleted')

    status = models.CharField(
        choices=PromoStatus.choices,
        default='T',
        max_length=1
    )
    text = models.TextField('Текст')
    discount = PositiveIntegerField('Скидка')

    def __str__(self):
        return self.text

    class Meta:
        verbose_name = 'Промокоды'
        verbose_name_plural = 'Промокоды'

class PurchasedExhibits(models.Model):
    exhibit = models.ForeignKey(Exhibits, on_delete=models.CASCADE, null=True, blank=True, default=None)
    price = PositiveIntegerField('Цена')

    def __str__(self):
        return self.exhibit

    class Meta:
        verbose_name = 'Товары, которые можно купить'
        verbose_name_plural = 'Товары, которые можно купить'

class Order(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    exhibits = models.ManyToManyField(PurchasedExhibits)
    price = PositiveIntegerField('Сумма')

    def __str__(self):
        return self.user.username

    class Meta:
        verbose_name = 'Заказы'
        verbose_name_plural = 'Заказы'

