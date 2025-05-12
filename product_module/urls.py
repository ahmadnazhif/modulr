# product_module/urls.py

from django.urls import path
from . import views

urlpatterns = [
    path('', views.product_list, name='product_landing_page'),
    path('<int:id>/', views.product_detail, name='product_detail'),
    path('create/', views.product_create, name='product_create'),
    path('<int:id>/edit/', views.product_update, name='product_update'),
    path('<int:id>/delete/', views.product_delete, name='product_delete'),
]
