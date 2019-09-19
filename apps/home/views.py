from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from apps.productos.models import *
from django.contrib.auth import login, logout

def home(request):
    context = {
        'productos': Producto.objects.filter(estado=True),
        'categorias': Categoria.objects.filter(estado=True),
        'subcategorias': Subcategoria.objects.filter(estado=True)
    }

    return render(request, 'home/home.html', context)
    
def filtrado(request, pk):
    context = {
        'productos': Producto.objects.filter(estado=True, subcategoria_id=pk),
        'categorias': Categoria.objects.filter(estado=True),
        'subcategorias': Subcategoria.objects.filter(estado=True)
    }

    return render(request, 'home/home.html', context)

def productos_descuento(request):
    context = {
        'productos': Descuento_Producto.objects.all(),
        'categorias': Categoria.objects.filter(estado=True),
        'subcategorias': Subcategoria.objects.filter(estado=True),
        'd': True
    }

    return render(request, 'home/home.html', context)

def filtrado_buscador(request):
    productos = Producto.objects.filter(nombre__icontains=request.POST['palabra'])

    context = {
        'productos': productos,
        'categorias': Categoria.objects.filter(estado=True),
        'subcategorias': Subcategoria.objects.filter(estado=True),
        'd': False
    }

    return render(request, 'home/home.html', context)