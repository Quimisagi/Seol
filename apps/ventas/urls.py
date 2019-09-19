from django.urls import path
from . import views
from django.contrib.auth import views as auth_views

app_name = 'ventas'
urlpatterns = [
    path('factura/', views.factura, name='factura'),
    path('pago/<int:pk>/', views.pago, name='pago'),
    path('confirmar_pago/', views.confirmar_pago, name='confirmar_pago'),
    path('historial_compras/<int:pk>/', views.historial_compras, name='historial_compras'),
]
