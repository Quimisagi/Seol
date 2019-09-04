from django.urls import path
from . import views

app_name = 'usuarios'
urlpatterns = [
    path('agregar/', views.registrar_usuario, name='agregar_usuario'),
    path('perfil/', views.editar_perfil, name='perfil'),
    path('listar/', views.listar_usuarios, name='listar_usuarios'),
    path('perfil/<int:pk>/eliminar/', views.eliminar_usuario.as_view(), name='eliminar_usuario'),
    path('perfil/<int:pk>/activar/', views.activar_usuario, name='activar_usuario'),
]