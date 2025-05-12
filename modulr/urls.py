from django.contrib import admin
from django.shortcuts import redirect
from django.urls import path, include
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('', lambda req: redirect('/module/')),
    path('auth/login/', auth_views.LoginView.as_view(template_name='auth/login.html'), name='login'),
    path('auth/logout/', auth_views.LogoutView.as_view(), name='logout'),
    path('admin/', admin.site.urls),
    path('module/', include('modular_engine.urls')),
    path('module/product/', include('product_module.urls')),
]
