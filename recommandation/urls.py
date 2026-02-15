from django.urls import path
from . import views

urlpatterns = [
    path('', views.home_view, name='home'),
    path('notification/', views.notif_view, name='notification'),
    path('notifications/department/<str:departement>/', views.department_messages, name='department_messages'),
    path('notifications/department/<str:departement>/page/<int:page>/', views.department_messages, name='department_messages_paginated'),
    path('notifications/departments',views.exe_departement_list,name='exe_departement-list'),
    path('notifications/message/<slug:slug>/', views.message_detail, name='message_detail'),
    path('a-propos/', views.about_us_view, name='about_us'),
]