from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from apps.productos.models import Categoria, Subcategoria, Producto
from django.contrib.auth import login, logout

def home(request):
    context = {
        'productos': Producto.objects.all(),
        'categorias': Categoria.objects.all(),
        'subcategorias': Subcategoria.objects.all()
    }

    return render(request, 'home/home.html', context)

