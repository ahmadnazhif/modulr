from django.urls import path
from . import views

urlpatterns = [
    path('', views.module_list, name='module_list'),
    path('install/<str:slug>/', views.module_install, name='module_install'),
    path('uninstall/<str:slug>/', views.module_uninstall, name='module_uninstall'),
    path('upgrade/<str:slug>/', views.module_upgrade, name='module_upgrade'),
]