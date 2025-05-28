from datetime import datetime, date

from dateutil.relativedelta import relativedelta
from django.contrib.auth.views import LogoutView
from django.contrib.auth.decorators import login_required
from django.db.models import Subquery
from django.http import HttpResponseNotFound
from django.shortcuts import redirect
from django.shortcuts import render
from django_tables2 import RequestConfig

from .filters import HallFilter, EmployeeFilter, ExhibitionFilter, ExcursionFilter
from .forms import HallForm, ExhibitForm, EmployeeForm, ExhibitionForm, ExcursionForm
from .models import Hall, Exhibits, ArtForm, Employees, TypeEmployee, Exhibition, Excursion
from .tables import HallTable, EmployeesTable, ExhibitionTable, ExcursionTable

@login_required
def secret_view(request):
    return render(request, 'secret.html')

class LogoutViaGet(LogoutView):
    def get(self, request, *args, **kwargs):
        return self.post(request, *args, **kwargs)

def index(request):
    return render(request, 'main/index.html')


def about(request):
    return render(request, 'main/about.html')


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
                exhibits = Exhibits.objects.filter( employee__full_name__contains=user.get_full_name())
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
            exhibit.name = request.POST.get('name')
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
        form = EmployeeForm(request.POST)
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
        if request.method == "POST":
            employee.full_name = request.POST.get('full_name')
            employee.birth_date = request.POST.get('birth_date')
            employee.phone = request.POST.get('phone')
            employee.type_id = request.POST.get('type')
            employee.hall_id = request.POST.get('hall')
            employee.save()
            return redirect('employees')
        else:
            return render(request, "main/edit-employee.html",
                          {
                              "employee": employee,
                              "types": types,
                              "halls": halls,
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
    table = ExcursionTable(f.qs,user=request.user)
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
