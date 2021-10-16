from django.contrib import admin
from django.urls import path
from home import views
urlpatterns = [
    # path('', views.index),
    path('', views.first, name='first'),
    path('login/', views.login, name='login'),
    path('receive/', views.receive),
    path('home', views.index, name='home'),
    path('about', views.about, name='about'),
    path('services', views.services, name='services'),
    path('contact', views.contact, name='contact'),
    path('order', views.order, name='order'),
    path('success', views.success, name='success'),
    path('product/<int:id>', views.product, name='productview'),
]
