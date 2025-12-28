from django.contrib.auth.views import LoginView
from django.urls import path

from . import views
from .views import custom_logout

urlpatterns = [

    path('login/', LoginView.as_view(template_name='main/login.html'), name='login'),
    path('logout/', custom_logout, name='logout'),

    path('', views.index, name='home'),
    path('about-us', views.about, name='about'),
    path('political-conf', views.political_conf, name='political-conf'),

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

    path('create-news', views.create_news, name='create-news'),
    path('news', views.news, name='news'),
    path('edit-news/<int:id>', views.edit_news, name='edit-news'),
    path('delete-news/<int:id>/', views.delete_news, name='delete-news'),

    path('create-faq', views.create_faq, name='create-faq'),
    path('faq', views.faq, name='faq'),
    path('edit-faq/<int:id>', views.edit_faq, name='edit-faq'),
    path('delete-faq/<int:id>/', views.delete_faq, name='delete-faq'),

    path('contacts', views.contacts, name='contacts'),

    path('create-vacancy', views.create_vacancy, name='create-vacancy'),
    path('vacancies', views.vacancies, name='vacancies'),
    path('vacancies/<int:id>', views.view_vacancy, name='view-vacancy'),
    path('edit-vacancy/<int:id>', views.edit_vacancy, name='edit-vacancy'),
    path('delete-vacancy/<int:id>/', views.delete_vacancy, name='delete-vacancy'),

    path('add-review', views.add_review, name='add-review'),
    path('reviews', views.reviews, name='reviews'),

    path('add-promocode', views.add_promocode, name='add-promocode'),
    path('promocodes', views.promocodes, name='promocodes'),
    path('return-promocodes/<int:id>', views.return_promocodes, name='return_promocodes'),
    path('archive-promocodes/<int:id>/', views.archive_promocodes, name='archive_promocodes'),
    path('delete-promocodes/<int:id>/', views.delete_promocodes, name='delete_promocodes'),
    path('delete-promocodes-force/<int:id>/', views.delete_promocodes_force, name='delete_promocodes_force'),

    path('interactivity', views.interactivity, name='interactivity'),

    path('purchased-exhibits, view', views.purchased_exhibits, name='purchased-exhibits'),
    path('basket', views.basket, name='basket'),
    path('make-order/', views.make_order, name='make-order'),
    path('check-promocode',views.check_promocode,name='check-promocode'),

    path('orders', views.show_my_orders, name='orders'),

]
