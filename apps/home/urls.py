from django.urls import path
from . import views
from django.contrib.auth import views as auth_views

app_name = 'home'
urlpatterns = [
    path('', views.home, name='home'),
    path('login/', auth_views.LoginView.as_view(template_name='home/login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(template_name='home/logout.html'), name='logout'),
    path('filtrado/<int:pk>/', views.filtrado, name='filtrado'),
    path('descuentos/', views.productos_descuento, name='descuentos'),
    path('filtrado_buscador/', views.filtrado_buscador, name='filtrado_buscador'),
]
