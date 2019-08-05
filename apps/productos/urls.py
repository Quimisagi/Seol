from django.urls import path
from . import views


app_name = 'productos'
urlpatterns = [
    path('menu/', views.menu_productos, name='menu_producto'),
    path('lista/', views.lista_producto, name='lista_producto'),
    path('agregar/', views.agregar_producto, name='agregar_producto'),
    path('<int:pk>/actualizar/', views.editar_producto, name='actu_producto'),
    path('<int:pk>/eliminar/', views.eliminar_producto.as_view(), name='eliminar_producto'),
    path('categoria/menu/', views.menu_categorias, name='menu_categoria'),
    path('categoria/lista/', views.lista_categoria, name='lista_categoria'),
    path('categoria/agregar/', views.agregar_categoria, name='agregar_categoria'),
    path('categoria/<int:pk>/actualizar/', views.editar_categoria, name='actu_categoria'),
    path('categoria/<int:pk>/eliminar/', views.eliminar_categoria.as_view(), name='eliminar_categoria'),
    path('subcategoria/<int:pk>/lista/', views.lista_subcategoria, name='lista_subcategoria'),
    path('subcategoria/<int:pk>/actualizar/', views.editar_subcategoria, name='actu_subcategoria'),
    path('subcategoria/<int:pk>/eliminar/', views.eliminar_subcategoria.as_view(), name='eliminar_subcategoria'),
    
]