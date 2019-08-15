from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from apps.productos.models import Categoria, Subcategoria, Producto
from django.contrib.auth import login, logout

def home(request):
    context = {
        'productos': Producto.objects.filter(estado=True),
        'categorias': Categoria.objects.filter(estado=True),
        'subcategorias': Subcategoria.objects.filter(estado=True)
    }

    return render(request, 'home/home.html', context)

