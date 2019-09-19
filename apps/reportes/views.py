from django.shortcuts import render
from apps.productos.models import *
from apps.ventas.models import *
from apps.usuarios.models import *
from django.db.models import Avg, Count, Min, Sum
from datetime import datetime
from django.contrib.auth.decorators import login_required, permission_required
from datetime import *; from dateutil.relativedelta import *
import calendar

@permission_required('productos.view_producto', login_url=None, raise_exception=True)
def menu(request):
    productos = Producto.objects.filter(estado=True)
    return render(request, 'reportes/menu.html', {'products': productos})

@permission_required('productos.view_producto', login_url=None, raise_exception=True)
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

@permission_required('productos.view_producto', login_url=None, raise_exception=True)
def reporte_mas_compras(request):
    facturas = Factura.objects.values('id_usuario').annotate(num=Sum('total')).filter(estado=True).order_by('-num')[:20]

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

@permission_required('productos.view_producto', login_url=None, raise_exception=True)
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

@permission_required('productos.view_producto', login_url=None, raise_exception=True)
def reporte_ventas_por_rango(request):
    if request.method == 'POST':
        fechas = request.POST['reservation']

        
        fecha_inicio = fechas.split("-")[0]
        f1 = fecha_inicio.split("/")[0]+"-"+fecha_inicio.split("/")[1]+"-"+fecha_inicio.split("/")[2]
        fecha_i = datetime.strptime(f1,"%Y-%m-%d").date()


        fecha_fin = fechas.split("-")[1]
        f2 = fecha_fin.split("/")[0]+"-"+fecha_fin.split("/")[1]+"-"+fecha_fin.split("/")[2]
        fecha_f = datetime.strptime(f2,"%Y-%m-%d").date()

        producto = Factura.objects.filter(fecha__range=(fecha_i, fecha_f), estado=True)
        total = 0
        for p in producto:
            total = total + p.total
        label = ['Total ventas']
        total2 = [float(total)]
        
        return render(request, 'reportes/barras.html', {'cantidad': total2, 'productos': label})
        
    else:
        producto = Factura.objects.filter(estado=True).aggregate(num=Sum('total'))
        
        total = [float(producto['num'])]
        label = ['Total ventas']

        return render(request, 'reportes/barras.html', {'cantidad': total, 'productos': label})

@permission_required('productos.view_producto', login_url=None, raise_exception=True)
def reporte_baja_existencia(request):
    productos = Producto.objects.filter(cantidad_disponible__lt=10, estado=True)

    return render(request, 'reportes/baja_cantidad.html', {'productos': productos})

@permission_required('productos.view_producto', login_url=None, raise_exception=True)
def reporte_cumpleanos(request):
    fecha = datetime.now()+relativedelta(months=+1)
    mes = fecha.month
    usuarios = Usuario.objects.filter(fecha_nacimiento__month=mes, estado=True)

    return render(request, 'reportes/cumpleanos.html', {'usuarios': usuarios})

@permission_required('productos.view_producto', login_url=None, raise_exception=True)
def producto_ventas(request, pk):
    p = Producto.objects.filter(estado=True)
    nombre = Producto.objects.get(id=pk)

    mes1 = (datetime.now()+relativedelta(months=-1)).month
    mes2 = (datetime.now()+relativedelta(months=-2)).month
    mes3 = (datetime.now()+relativedelta(months=-3)).month
    mes4 = (datetime.now()+relativedelta(months=-4)).month
    mes5 = (datetime.now()+relativedelta(months=-5)).month
    mes6 = (datetime.now()+relativedelta(months=-6)).month

    producto_mes1 = Factura_Producto.objects.values('producto_id').annotate(num=Sum('subtotal')).filter(producto_id=pk, factura__fecha__month=mes1)
    producto_mes2 = Factura_Producto.objects.values('producto_id').annotate(num=Sum('subtotal')).filter(producto_id=pk, factura__fecha__month=mes2) 
    producto_mes3 = Factura_Producto.objects.values('producto_id').annotate(num=Sum('subtotal')).filter(producto_id=pk, factura__fecha__month=mes3)
    producto_mes4 = Factura_Producto.objects.values('producto_id').annotate(num=Sum('subtotal')).filter(producto_id=pk, factura__fecha__month=mes4)
    producto_mes5 = Factura_Producto.objects.values('producto_id').annotate(num=Sum('subtotal')).filter(producto_id=pk, factura__fecha__month=mes5)
    producto_mes6 = Factura_Producto.objects.values('producto_id').annotate(num=Sum('subtotal')).filter(producto_id=pk, factura__fecha__month=mes6)

    pr = [producto_mes1, producto_mes2, producto_mes3, producto_mes4, producto_mes5, producto_mes6]
    valores = []
    for m in pr:
        if m:
            for n in m:
                valores.append(float(n['num']))
        else:
            valores.append(0)
        
            
    
    valores.reverse()
    meses = [switch_mes(mes6), switch_mes(mes5), switch_mes(mes4), switch_mes(mes3), switch_mes(mes2), switch_mes(mes1)]

    
    return render(request, 'reportes/barras_producto.html', {'products': p, 'cantidad': valores, 'productos': meses, 'nombre': nombre.nombre })

def switch_mes(argument):
    switcher = {
        1: "Enero",
        2: "Febrero",
        3: "Marzo",
        4: "Abril",
        5: "Mayo",
        6: "Junio",
        7: "Julio",
        8: "Agosto",
        9: "Septiembre",
        10: "Octobre",
        11: "Noviembre",
        12: "Diciembre"
    }
    return switcher.get(argument, "Invalid month")