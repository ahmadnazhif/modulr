from django.urls import path
from . import views

urlpatterns = [
    path('modules/', views.module_list, name='module_list'),
    path('module/<str:module_name>/install/', views.module_install, name='module_install'),
    path('module/<str:module_name>/uninstall/', views.module_uninstall, name='module_uninstall'),
    path('module/<str:module_name>/upgrade/', views.module_upgrade, name='module_upgrade'),
]