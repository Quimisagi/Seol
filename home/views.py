from django.shortcuts import render
from django.http import HttpResponse

productos = [
    {
        'Nombre': 'Piano de cola',
        'Marca': 'Panasonic',
        'Precio': '$6´000.000'
        #'Imagen': "static/img/avatar.png"
    },
    {
        'Nombre': 'Guitarra',
        'Marca': 'Sony',
        'Precio': '$300.000'
        #'Imagen': "static/img/avatar2.png"
    }
]

def home(request):
    context = {
        'productos': productos
    }
    return render(request, 'home.html', context)

