from django.urls import path

from . import views
from django.contrib import admin
from django.urls import include, path

urlpatterns = [
    path('', views.index, name='index'),
    path('search/', views.search, name='search'),
    path('result/', views.result, name='result'),
    path('search/send_contact/', views.send_contact, name='send_contact'),
    path('search/send_report/', views.send_report, name='send_report'),
    path('church/<int:church_id>/', views.church, name='church'),
    path('group/<int:group_id>/', views.group, name='group'),
    path('search/get/group/', views.allGroup, name='allGroup'),
    path('search/get/church/', views.allChurch, name='allChurch'),
    path('search/get/school/', views.allSchool, name='allSchool'),
]