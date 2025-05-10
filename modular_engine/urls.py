from django.urls import path
from . import views

urlpatterns = [
    path('', views.module_list, name='module_list'),
    path('<str:module_name>/install/', views.module_install, name='module_install'),
    path('<str:module_name>/uninstall/', views.module_uninstall, name='module_uninstall'),
    path('<str:module_name>/upgrade/', views.module_upgrade, name='module_upgrade'),
]