from django.urls import path
from . import views
from django.contrib.auth import views as auth_views

app_name = 'reportes'
urlpatterns = [
    path('menu/', views.menu, name='menu'), 
    path('reporte_mas_vendidos/', views.reporte_mas_vendidos, name='reporte_mas_vendidos'),
    path('reporte_menos_vendidos/', views.reporte_menos_vendidos, name='reporte_menos_vendidos'),
    path('reporte_mas_compras/', views.reporte_mas_compras, name='reporte_mas_compras'),
    path('reporte_ventas_por_rango/', views.reporte_ventas_por_rango, name='reporte_ventas_por_rango'),
    path('reporte_baja_existencia/', views.reporte_baja_existencia, name='reporte_baja_existencia'),
    path('reporte_cumpleanos/', views.reporte_cumpleanos, name='reporte_cumpleanos'),
    path('producto_ventas/<int:pk>/', views.producto_ventas, name='producto_ventas'),

]

