from django.contrib.auth.views import LoginView, LogoutView
from django.urls import path

from . import views
from .views import LogoutViaGet

urlpatterns = [

    path('login/', LoginView.as_view(template_name='main/login.html'), name='login'),
    path('logout/', LogoutViaGet.as_view(), name='logout'),

    path('', views.index, name='home'),
    path('about-us', views.about, name='about'),

    path('create-hall', views.create_hall, name='create-hall'),
    path('halls', views.halls, name='halls'),
    path("edit-hall/<int:id>", views.edit_hall, name='edit-hall'),
    path("delete-hall/<int:id>/", views.delete_hall, name='delete-hall'),

    path('create-exhibit', views.create_exhibit, name='create-exhibit'),
    path('exhibits', views.exhibits, name='exhibits'),
    path("edit-exhibit/<int:id>", views.edit_exhibit, name='edit-exhibit'),
    path("delete-exhibit/<int:id>/", views.delete_exhibit, name='delete-exhibit'),

    path('create-employee', views.create_employee, name='create-employee'),
    path('employees', views.employees, name='employees'),
    path("edit-employee/<int:id>", views.edit_employee, name='edit-employee'),
    path("delete-employee/<int:id>/", views.delete_employee, name='delete-employee'),

    path('create-exhibition', views.create_exhibition, name='create-exhibition'),
    path('exhibition', views.exhibition, name='exhibition'),
    path("edit-exhibition/<int:id>", views.edit_exhibition, name='edit-exhibition'),
    path("delete-exhibition/<int:id>/", views.delete_exhibition, name='delete-exhibition'),

    path('create-excursion', views.create_excursion, name='create-excursion'),
    path('excursions', views.excursions, name='excursions'),
    path("edit-excursion/<int:id>", views.edit_excursion, name='edit-excursion'),
    path("delete-excursion/<int:id>/", views.delete_excursion, name='delete-excursion'),

]
