from django.urls import path
from . import views

app_name = 'carrito'
urlpatterns = [
    path('', views.carrito, name='carrito'),
    path('agregar/<int:pk>/<int:cn>/', views.agregar_carrito, name='agregar_carrito'),
    path('eliminar/<int:pk>/', views.eliminar_carrito, name='eliminar_carrito'),
    path('actualizar/<int:pk>/<int:accion>', views.actualizar_carrito, name='actualizar_carrito'),
]