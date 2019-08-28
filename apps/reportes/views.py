from django.shortcuts import render
from apps.productos.models import *
from apps.ventas.models import *
from apps.usuarios.models import *
from django.db.models import Avg, Count, Min, Sum
from datetime import datetime

def menu(request):
    return render(request, 'reportes/menu.html', {})
 
def reporte_mas_vendidos(request):
    producto = Factura_Producto.objects.values('producto').annotate(num=Sum('cantidad')).order_by('-num')[:20]

    productos = []
    cantidad = []

    for p in producto:
        pr = Producto.objects.get(id=p['producto'])
        productos.append(pr.nombre)
        cantidad.append(p['num'])
    n = len(cantidad)
    
    context = {
        'productos': productos,
        'cantidad': cantidad,
        'tamaño': n,
        'titulo': "PRODUCTOS MÁS VENDIDOS"
    }
    return render(request, 'reportes/prueba.html', context) 

def reporte_mas_compras(request):
    facturas = Factura.objects.values('id_usuario').annotate(num=Sum('total')).order_by('-num')[:20]

    clientes = []
    cantidad = []

    for f in facturas:
        c = Usuario.objects.get(id=f['id_usuario'])
        clientes.append(c.nombres)
        cantidad.append(float(f['num']))
    n = len(cantidad)

    context = {
        'productos': clientes,
        'cantidad': cantidad,
        'tamaño': n,
        'titulo': "CLIENTES QUE MÁS HAN COMPRADO"
    }
    return render(request, 'reportes/prueba.html', context) 

def reporte_menos_vendidos(request):

    producto = Factura_Producto.objects.values('producto').annotate(num=Sum('cantidad')).order_by('num')[:20]

    productos = []
    cantidad = []
    
    for p in producto:
        pr = Producto.objects.get(id=p['producto'])
        productos.append(pr.nombre)
        cantidad.append(p['num'])
    n = len(cantidad)
    
    context = {
        'productos': productos,
        'cantidad': cantidad,
        'tamaño': n,
        'titulo': "PRODUCTOS MENOS VENDIDOS"
    }

    return render(request, 'reportes/prueba.html', context) 

def reporte_ventas_por_rango(request):
    if request.method == 'POST':
        fechas = request.POST['reservation']

        
        fecha_inicio = fechas.split("-")[0]
        f1 = fecha_inicio.split("/")[2]+"-"+fecha_inicio.split("/")[0]+"-"+fecha_inicio.split("/")[1]
        fecha_i = datetime.strptime(f1,"%Y-%m-%d").date()


        fecha_fin = fechas.split("-")[1]
        f2 = fecha_fin.split("/")[2]+"-"+fecha_fin.split("/")[0]+"-"+fecha_fin.split("/")[1]
        fecha_f = datetime.strptime(f2,"%Y-%m-%d").date()

        producto = Factura.objects.filter(fecha__range=(fecha_i, fecha_f))
        total = 0
        for p in producto:
            total = total + p.total
        label = ['Total ventas']
        total2 = [float(total)]
        
        return render(request, 'reportes/barras.html', {'cantidad': total2, 'productos': label})
        
    else:
        producto = Factura.objects.aggregate(num=Sum('total'))
        print(producto)
        total = [float(producto['num'])]
        label = ['Total ventas']

        return render(request, 'reportes/barras.html', {'cantidad': total, 'productos': label})

def reporte_baja_existencia(request):
    productos = Producto.objects.filter(cantidad_disponible__lt=10)

    return render(request, 'reportes/baja_cantidad.html', {'productos': productos})

def reporte_cumpleanos(request):
    mes = datetime.now().month
    usuarios = Usuario.objects.filter(fecha_nacimiento__month=mes)

    return render(request, 'reportes/cumpleanos.html', {'usuarios': usuarios})


