"""Seol URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.contrib.auth import views as auth_views
from django.urls import path, include
from apps.usuarios import views as usuario_views
from apps.productos import views as producto_views
from django.conf import settings
from django.conf.urls.static import static
from apps.usuarios.views import PostDeleteView
from apps.productos.views import ProductDeleteView, CategoryDeleteView


urlpatterns = [
    path('admin/', admin.site.urls),
    path('register/', usuario_views.register, name='register'),
    path('profile/', usuario_views.profile, name='profile'),
    path('producto/', producto_views.menuProductos, name='menu_producto'),
    path('producto/lista', producto_views.productList, name='lista_producto'),
    path('producto/<int:pk>/actualizar', producto_views.productUpdate, name='actu_producto'),
    path('producto/<int:pk>/delete', ProductDeleteView.as_view(), name='delete_producto'),
    path('producto/agregar', producto_views.productRegister, name='agregar_producto'),
    path('categoria/', producto_views.menuCategorias, name='menu_categoria'),
    path('categoria/lista', producto_views.categoryList, name='lista_categoria'),
    path('subcategoria/<int:pk>/lista', producto_views.subcategoryList, name='lista_subcategoria'),
    path('subcategoria/<int:pk>/actualizar', producto_views.subcategoryUpdate, name='actu_subcategoria'),
    path('categoria/agregar', producto_views.categoryRegister, name='agregar_categoria'),
    path('categoria/<int:pk>/actualizar', producto_views.categoryUpdate, name='actu_categoria'),
    path('categoria/<int:pk>/delete', CategoryDeleteView.as_view(), name='delete_categoria'),
    path('profile/<int:pk>/delete/', PostDeleteView.as_view(), name='delete_user'),
    path('login/', auth_views.LoginView.as_view(template_name='home/login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(template_name='home/logout.html'), name='logout'),
    path('', include('apps.home.urls')),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
