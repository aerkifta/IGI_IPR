import json
from datetime import datetime, date

from dateutil.relativedelta import relativedelta
from django.contrib import messages
from django.contrib.auth import logout
from django.contrib.auth.decorators import login_required
from django.db.models import Subquery
from django.http import HttpResponseNotFound, JsonResponse
from django.shortcuts import redirect
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from django_tables2 import RequestConfig

from .filters import HallFilter, EmployeeFilter, ExhibitionFilter, ExcursionFilter
from .forms import HallForm, ExhibitForm, EmployeeForm, ExhibitionForm, ExcursionForm, NewsForm, FAQForm, VacancyForm, \
    ReviewForm, PromoCodesForm
from .models import Hall, Exhibits, ArtForm, Employees, TypeEmployee, Exhibition, Excursion, News, FAQ, \
    EmployeeContacts, Vacancy, Reviews, PromoCodes, PurchasedExhibits, Order
from .tables import HallTable, EmployeesTable, ExhibitionTable, ExcursionTable


@csrf_exempt
def custom_logout(request):
    logout(request)
    return redirect('login')


def index(request):
    return render(request, 'main/index.html')


def about(request):
    return render(request, 'main/about.html')


def political_conf(request):
    return render(request, 'main/political-conf.html')


# @user_passes_test(lambda u: u.is_superuser)
def halls(request):
    f = HallFilter(request.GET, queryset=Hall.objects.all())
    table = HallTable(f.qs)
    per_page = request.GET.get("per_page")
    if per_page:
        RequestConfig(request, paginate={"per_page": per_page}).configure(table)
    else:
        RequestConfig(request, paginate={"per_page": 5}).configure(table)
    return render(request, 'main/halls.html', {'filter': f, 'table': table})
    # table = HallTable(Hall.objects.all())
    # RequestConfig(request).configure(table)
    # return render(request, 'main/halls.html', {'table': table})
    # if request.method == 'POST':
    #     keyword = request.POST['keyword']
    #     halls = Hall.objects.filter(description__contains=keyword) | Hall.objects.filter(title__icontains=keyword)
    # else:
    #     halls = Hall.objects.order_by('description')
    # return render(request, 'main/halls.html', {'title': 'Залы', 'halls': halls})


# @user_passes_test(lambda u: u.is_superuser)
def create_hall(request):
    error = ''
    if request.method == 'POST':
        form = HallForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('halls')
        else:
            error = 'Форма неверная'

    form = HallForm()
    context = {
        'form': form,
        'error': error
    }
    return render(request, 'main/create-hall.html', context)


# @user_passes_test(lambda u: u.is_superuser)
def edit_hall(request, id):
    try:
        hall = Hall.objects.get(id=id)
        if request.method == "POST":
            hall.number = int(request.POST.get('number', 0))
            hall.title = request.POST.get('title')
            hall.description = request.POST.get('description')
            hall.level = int(request.POST.get('level', 0))
            hall.square = float(request.POST.get('square', 0))
            hall.save()
            return redirect('halls')
        else:
            hall.square = str(hall.square)
            return render(request, "main/edit-hall.html", {"hall": hall})
    except Hall.DoesNotExist:
        return HttpResponseNotFound("<h2>Hall not found</h2>")


# @user_passes_test(lambda u: u.is_superuser)
def delete_hall(request, id):
    try:
        hall = Hall.objects.get(id=id)
        hall.delete()
        return redirect('halls')
    except Hall.DoesNotExist:
        return HttpResponseNotFound("<h2>Hall not found</h2>")


# @user_passes_test(lambda u: u.is_staff and u.is_superuser)
def exhibits(request):
    user = request.user
    if request.method == 'POST':
        keyword = request.POST['keyword']
        if user.is_staff:
            exhibits = (Exhibits.objects.filter(description__contains=keyword)
                        | Exhibits.objects.filter(name__icontains=keyword) | Exhibits.objects.filter(
                        employee__full_name__contains=user.get_full_name()))
        else:
            exhibits = (Exhibits.objects.filter(description__contains=keyword)
                        | Exhibits.objects.filter(name__icontains=keyword))
    else:
        if request.GET.get('latest'):
            if user.is_staff:
                exhibits = Exhibits.objects.filter(
                    period__gt=(datetime.today() - relativedelta(months=6))) | Exhibits.objects.filter(
                    employee__full_name__contains=user.get_full_name())
            else:
                exhibits = Exhibits.objects.filter(
                    period__gt=(datetime.today() - relativedelta(months=6)))
        else:
            if user.is_staff:
                exhibits = Exhibits.objects.filter(employee__full_name__contains=user.get_full_name())
            else:
                exhibits = Exhibits.objects.all()
    return render(request, 'main/exhibits.html', {'title': 'Экспонаты', 'exhibits': exhibits})

    # @user_passes_test(lambda u: u.is_superuser)


def create_exhibit(request):
    error = ''
    if request.method == 'POST':
        form = ExhibitForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('exhibits')
        else:
            error = 'Форма неверная'

    form = ExhibitForm()
    context = {
        'form': form,
        'error': error
    }
    return render(request, 'main/create-exhibit.html', context)

    # @user_passes_test(lambda u: u.is_superuser)


def edit_exhibit(request, id):
    try:
        exhibit = Exhibits.objects.get(id=id)
        art_form = ArtForm.objects.all()
        employees = Employees.objects.filter(type__name="Смотрящий")
        if request.method == "POST":
            exhibit.title = request.POST.get('name')
            exhibit.description = request.POST.get('description')
            exhibit.period = request.POST.get('period')
            exhibit.art_form_id = request.POST.get('art_form')
            exhibit.employee_id = request.POST.get('employee')
            image = request.FILES.get('image')
            if image:
                exhibit.image = image
            exhibit.save()
            return redirect('exhibits')
        else:
            return render(request, "main/edit-exhibit.html",
                          {"exhibit": exhibit, "art_forms": art_form, "employees": employees,
                           "max_date": date.today()})
    except Exhibits.DoesNotExist:
        return HttpResponseNotFound("<h2>Exhibit not found</h2>")

    # @user_passes_test(lambda u: u.is_superuser)


def delete_exhibit(request, id):
    try:
        exhibit = Exhibits.objects.get(id=id)
        exhibit.delete()
        return redirect('exhibits')
    except Hall.DoesNotExist:
        return HttpResponseNotFound("<h2>Exhibit not found</h2>")

    # @user_passes_test(lambda u: u.is_superuser)


def employees(request):
    f = EmployeeFilter(request.GET, queryset=Employees.objects.all())
    table = EmployeesTable(f.qs)
    per_page = request.GET.get("per_page")
    if per_page:
        RequestConfig(request, paginate={"per_page": per_page}).configure(table)
    else:
        RequestConfig(request, paginate={"per_page": 5}).configure(table)
    return render(request, 'main/employees.html', {'filter': f, 'table': table})

    # @user_passes_test(lambda u: u.is_superuser)


def create_employee(request):
    error = ''
    if request.method == 'POST':
        form = EmployeeForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('employees')
        else:
            error = 'Форма неверная'

    form = EmployeeForm()
    context = {
        'form': form,
        'error': error
    }
    return render(request, 'main/create-employee.html', context)

    # @user_passes_test(lambda u: u.is_superuser)


def edit_employee(request, id):
    try:
        employee = Employees.objects.get(id=id)
        types = TypeEmployee.objects.all()
        halls = Hall.objects.all()

        contacts, created = EmployeeContacts.objects.get_or_create(employee=employee)
        if request.method == "POST":
            employee.full_name = request.POST.get('full_name')
            employee.birth_date = request.POST.get('birth_date')
            employee.phone = request.POST.get('phone')
            employee.type_id = request.POST.get('type')
            employee.hall_id = request.POST.get('hall')
            employee.save()

            contacts.work_phone = request.POST.get('work_phone')
            contacts.email = request.POST.get('email')
            contacts.description = request.POST.get('description')
            contacts.is_visible = bool(request.POST.get('is_visible'))

            if request.FILES.get('image'):
                contacts.image = request.FILES.get('image')

            contacts.save()

            return redirect('employees')
        else:
            return render(request, "main/edit-employee.html",
                          {
                              "employee": employee,
                              "types": types,
                              "halls": halls,
                              "contacts": contacts,
                              "max_date": date.today() - relativedelta(years=18),
                              "min_date": date.today() - relativedelta(years=80)})
    except Exhibits.DoesNotExist:
        return HttpResponseNotFound("<h2>Exhibit not found</h2>")

    # @user_passes_test(lambda u: u.is_superuser)


def delete_employee(request, id):
    try:
        employee = Employees.objects.get(id=id)
        employee.delete()
        return redirect('employees')
    except Employees.DoesNotExist:
        return HttpResponseNotFound("<h2>Employee not found</h2>")

    # @user_passes_test(lambda u: u.is_superuser)


def exhibition(request):
    f = ExhibitionFilter(request.GET, queryset=Exhibition.objects.all())
    table = ExhibitionTable(f.qs)
    per_page = request.GET.get("per_page")
    if per_page:
        RequestConfig(request, paginate={"per_page": per_page}).configure(table)
    else:
        RequestConfig(request, paginate={"per_page": 5}).configure(table)
    return render(request, 'main/exhibition.html', {'filter': f, 'table': table})

    # @user_passes_test(lambda u: u.is_superuser)


def create_exhibition(request):
    error = ''
    if request.method == 'POST':
        form = ExhibitionForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('exhibition')
        else:
            error = 'Форма неверная'

    form = ExhibitionForm()
    context = {
        'form': form,
        'error': error
    }
    return render(request, 'main/create-exhibition.html', context)

    # @user_passes_test(lambda u: u.is_superuser)


def edit_exhibition(request, id):
    try:
        exhibition = Exhibition.objects.get(id=id)
        exhibits = Exhibits.objects.all()

        if request.method == "POST":
            exhibition.name = request.POST.get('name')
            exhibition.date_from = request.POST.get('date_from')
            exhibition.date_to = request.POST.get('date_to')
            selected_ids = request.POST.getlist('exhibits')
            exhibition.exhibits.set(selected_ids)
            exhibition.save()
            return redirect('exhibition')
        else:
            return render(request, "main/edit-exhibition.html",
                          {
                              "exhibition": exhibition,
                              "exhibits": exhibits})
    except Exhibition.DoesNotExist:
        return HttpResponseNotFound("<h2>Exhibition not found</h2>")

    # @user_passes_test(lambda u: u.is_superuser)


def delete_exhibition(request, id):
    try:
        exhibition = Exhibition.objects.get(id=id)
        exhibition.delete()
        return redirect('exhibition')
    except Exhibition.DoesNotExist:
        return HttpResponseNotFound("<h2>Exhibition not found</h2>")

    # @user_passes_test(lambda u: u.is_superuser and u.is_staff)


def excursions(request):
    excursions = Excursion.objects.all()
    if request.user.is_staff:
        excursions = Excursion.objects.filter(employee__full_name__contains=request.user.get_full_name())
    f = ExcursionFilter(request.GET, queryset=excursions)
    table = ExcursionTable(f.qs, user=request.user)
    per_page = request.GET.get("per_page")
    if per_page:
        RequestConfig(request, paginate={"per_page": per_page}).configure(table)
    else:
        RequestConfig(request, paginate={"per_page": 5}).configure(table)
    return render(request, 'main/excursions.html', {'filter': f, 'table': table})

    # @user_passes_test(lambda u: u.is_superuser)


def create_excursion(request):
    error = ''
    if request.method == 'POST':
        form = ExcursionForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('excursions')
        else:
            error = 'Форма неверная'

    form = ExcursionForm()
    context = {
        'form': form,
        'error': error
    }
    return render(request, 'main/create-excursion.html', context)

    # @user_passes_test(lambda u: u.is_superuser)


def edit_excursion(request, id):
    try:
        excursion = Excursion.objects.get(id=id)
        employees = Employees.objects.filter(type__name="Экскурсовод")
        exhibition = Exhibition.objects.exclude(id=Subquery(Excursion.objects.values('id')))
        if request.method == "POST":
            excursion.name = request.POST.get('name')
            if excursion.exhibition_id != int(request.POST.get('exhibition')):
                excursion.exhibition_id = request.POST.get('exhibition')
            excursion.employee_id = request.POST.get('employee')
            excursion.save()
            return redirect('excursions')
        else:
            return render(request, "main/edit-excursion.html",
                          {
                              "excursion": excursion,
                              "exhibition": exhibition,
                              "employees": employees})
    except Exhibition.DoesNotExist:
        return HttpResponseNotFound("<h2>Excursion not found</h2>")

    # @user_passes_test(lambda u: u.is_superuser)


def delete_excursion(request, id):
    try:
        excursion = Excursion.objects.get(id=id)
        excursion.delete()
        return redirect('excursions')
    except Exhibition.DoesNotExist:
        return HttpResponseNotFound("<h2>excursion not found</h2>")


def create_news(request):
    error = ''
    if request.method == 'POST':
        form = NewsForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('news')
        else:
            error = 'Форма неверная'

    form = NewsForm()
    context = {
        'form': form,
        'error': error
    }
    return render(request, 'main/create-news.html', context)


def news(request):
    queryset = News.objects.all()
    return render(request, "main/news.html", context={
        "news": queryset,
        "title": "Новости"})


def edit_news(request, id):
    try:
        query_news = News.objects.get(id=id)
        if request.method == "POST":
            query_news.name = request.POST.get('name')
            query_news.summary = request.POST.get('summary')
            query_news.description = request.POST.get('description')
            image = request.FILES.get('image')
            if image:
                query_news.image = image
            query_news.save()
            return redirect('news')
        else:
            return render(request, "main/edit-news.html",
                          {"news": query_news})
    except News.DoesNotExist:
        return HttpResponseNotFound("<h2>Новость не найдена</h2>")

    # @user_passes_test(lambda u: u.is_superuser)


def delete_news(request, id):
    try:
        query_news = News.objects.get(id=id)
        query_news.delete()
        return redirect('news')
    except News.DoesNotExist:
        return HttpResponseNotFound("<h2>Новость не найдена</h2>")

    # @user_passes_test(lambda u: u.is_superuser)


def create_faq(request):
    error = ''
    if request.method == 'POST':
        form = FAQForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('faq')
        else:
            error = 'Форма неверная'

    form = FAQForm()
    context = {
        'form': form,
        'error': error
    }
    return render(request, 'main/create-faq.html', context)


def faq(request):
    queryset = FAQ.objects.all()
    return render(request, "main/faq.html", context={
        "faq": queryset,
        "title": "FAQ"})


def edit_faq(request, id):
    try:
        query_faq = FAQ.objects.get(id=id)
        if request.method == "POST":
            query_faq.question = request.POST.get('question')
            query_faq.answer = request.POST.get('answer')
            query_faq.save()
            return redirect('faq')
        else:
            return render(request, "main/edit-faq.html",
                          {"faq": query_faq})
    except FAQ.DoesNotExist:
        return HttpResponseNotFound("<h2>FAQ не найдена</h2>")


def delete_faq(request, id):
    try:
        query_faq = FAQ.objects.get(id=id)
        query_faq.delete()
        return redirect('faq')
    except FAQ.DoesNotExist:
        return HttpResponseNotFound("<h2>FAQ не найдена</h2>")

    # @user_passes_test(lambda u: u.is_superuser)


def contacts(request):
    query_set = Employees.objects.filter(employeecontacts__is_visible=True)
    return render(request, 'main/contacts.html', context={'contacts': query_set})


def create_vacancy(request):
    error = ''
    if request.method == 'POST':
        form = VacancyForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('vacancies')
        else:
            error = 'Форма неверная'

    form = VacancyForm()
    context = {
        'form': form,
        'error': error
    }
    return render(request, 'main/create-vacancy.html', context)


def vacancies(request):
    queryset = Vacancy.objects.all()
    return render(request, "main/vacancies.html", context={
        "vacancies": queryset,
        "title": "Вакансии"})


def view_vacancy(request, id):
    try:
        user = request.user
        query_vacancy = Vacancy.objects.get(id=id)
        if not user.is_staff or not user.is_superuser:
            query_vacancy.response_count = query_vacancy.response_count + 1
            query_vacancy.save()
        return render(request, 'main/vacancy.html',
                      context={'vacancy': query_vacancy})
    except Vacancy.DoesNotExist:
        return HttpResponseNotFound("<h2>Вакансия не найдена</h2>")


def edit_vacancy(request, id):
    try:
        query_vacancy = Vacancy.objects.get(id=id)
        if request.method == "POST":
            query_vacancy.name = request.POST.get('name')
            query_vacancy.description = request.POST.get('description')
            query_vacancy.salary = request.POST.get('salary')
            query_vacancy.save()
            return redirect('vacancies')
        else:
            return render(request, "main/edit-vacancy.html",
                          {"vacancy": query_vacancy})
    except Vacancy.DoesNotExist:
        return HttpResponseNotFound("<h2>Вакансия не найдена</h2>")


def delete_vacancy(request, id):
    try:
        query_vacancy = Vacancy.objects.get(id=id)
        query_vacancy.delete()
        return redirect('vacancies')
    except Vacancy.DoesNotExist:
        return HttpResponseNotFound("<h2>Вакансия не найдена</h2>")


def add_review(request):
    error = ''
    if request.method == 'POST':
        form = ReviewForm(request.POST)
        if form.is_valid():
            review = form.save(commit=False)
            review.author = request.user
            review.save()
            form.save()
            return redirect('reviews')
        else:
            error = 'Форма неверная'

    form = ReviewForm()
    context = {
        'form': form,
        'error': error,
        'title': 'Оставить отзыв'
    }
    return render(request, 'main/add-review.html', context)


def reviews(request):
    query_set = Reviews.objects.all().order_by('-created_at')
    filter_option = request.GET.get('filter')

    if filter_option == 'my_reviews':
        query_set = query_set.filter(author=request.user)
    elif filter_option == 'latest':
        query_set = query_set.order_by('-created_at')

    return render(request, 'main/reviews.html', {
        'reviews': query_set,
        'title': 'Отзывы',
    })


def add_promocode(request):
    user = request.user

    if not (user.is_staff or user.is_superuser):
        return redirect('promocodes')

    if request.method == 'POST':
        form = PromoCodesForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('promocodes')
    else:
        form = PromoCodesForm()

    return render(request, 'main/add_promocode.html', {'form': form, 'title': 'Добавить промокод'})


def promocodes(request):
    user = request.user
    if user.is_staff or user.is_superuser:
        query_set = PromoCodes.objects.all()
    else:
        query_set = PromoCodes.objects.filter(status=PromoCodes.PromoStatus.ACTIVE)

    return render(request, 'main/promocode.html',
                  {'promocodes': query_set,
                   'title': 'Промокоды'})


def return_promocodes(request, id):
    promo_code = PromoCodes.objects.get(id=id)
    promo_code.status = PromoCodes.PromoStatus.ACTIVE
    promo_code.save()
    return redirect('promocodes')


def archive_promocodes(request, id):
    promo_code = PromoCodes.objects.get(id=id)
    promo_code.status = PromoCodes.PromoStatus.ARCHIVED
    promo_code.save()
    return redirect('promocodes')


def delete_promocodes(request, id):
    promo_code = PromoCodes.objects.get(id=id)
    promo_code.status = PromoCodes.PromoStatus.DELETED
    promo_code.save()
    return redirect('promocodes')


def delete_promocodes_force(request, id):
    PromoCodes.objects.get(id=id).delete()
    return redirect('promocodes')


def interactivity(request):
    return render(request, 'main/interactivity.html')


def purchased_exhibits(request):
    query_set = PurchasedExhibits.objects.all()
    return render(request, 'main/purchased-exhibits.html', {'purchased_exhibits': query_set,
                                                            'title': 'Экспонаты, которые можно приобрести'})


def basket(request):
    return render(request, 'main/basket.html')


@csrf_exempt
def check_promocode(request):
    data = json.loads(request.body)
    code = data.get("code", "").strip()

    try:
        promo = PromoCodes.objects.filter(text=code, status='T').first()
        return JsonResponse({"valid": True, "discount": promo.discount})
    except PromoCodes.DoesNotExist:
        return JsonResponse({"valid": False})


@login_required
def make_order(request):
    if request.method == "POST":
        items_json = request.POST.get("items_json")
        items = json.loads(items_json)
        discount = int(request.POST.get("discount", 0))

        total = sum(float(i["price"]) for i in items)

        if discount:
            total = total - (total * discount / 100)

        order = Order.objects.create(
            user=request.user,
            price=total
        )

        for i in items:
            order.exhibits.add(i["id"])

        order.save()

        messages.success(request, "Ваш заказ успешно оформлен!")

        return redirect('orders')

    return redirect('cart')


def show_my_orders(request):
    user = request.user
    query_set = Order.objects.filter(user=user)
    return render(request, 'main/orders.html', {'orders': query_set,
                                                'title': 'Мои заказы'})
