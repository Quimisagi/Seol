from django.shortcuts import render, redirect, get_object_or_404
from apps.carrito.models import Carrito_Compras_Producto, Carrito_Compras
from apps.usuarios.models import Usuario
from django.contrib import messages
from apps.productos.models import Producto
from .forms import Confirmar_Datos, F_Factura_Pago
from .models import *
import datetime
from django.forms import modelformset_factory



def factura(request):
    if request.method == 'POST':

        form = Confirmar_Datos(request.POST)

        if form.is_valid():
            usuario = request.user
            usuarioNombre = form.cleaned_data.get('nombres')
            usuarioApellido = form.cleaned_data.get('apellidos')
            usuarioDireccion = form.cleaned_data.get('direccion')
            usuarioTelefono = form.cleaned_data.get('telefono')
            usuarioCiudad = form.cleaned_data.get('ciudad')

            carrito = request.user.carrito_compras.id
            productos = Carrito_Compras_Producto.objects.filter(carrito=carrito)
            total = 0
            for producto in productos:
                total = total + producto.subtotal
            iva = (total * 19)/100
            envio = 5000
            totaliva = total + iva + envio 

            x = datetime.datetime.now()
            fecha_hoy = ("%s/%s/%s" % (x.day, x.month, x.year))

            factura = Factura(id_usuario=usuario.id,nombre_usuario=usuarioNombre, apellido_usuario=usuarioApellido, direccion_usuario=usuarioDireccion, telefono_usuario=usuarioTelefono, ciudad_usuario=usuarioCiudad, fecha=fecha_hoy, total=totaliva)
            factura.save()
            
            for p in productos:
                Factura_Producto(factura=factura, producto=p.producto, cantidad=p.cantidad, subtotal=p.subtotal).save()
            

            context = {
                'carritop': productos,
                'total': total,
                'iva': iva,
                'envio': envio,
                'usuario': usuario,
                'factura': factura
            }
            
            

            return render(request, 'ventas/factura.html', context)  
    else:
        form = Confirmar_Datos()
        usuario = request.user
        return render(request, 'ventas/confirmar_datos.html', {'form': form, 'usuario': usuario})
    
    
def pago(request, pk):
    """
    factura = Factura.objects.get(id=pk)
    factura.estado = True
    factura.save()
    carrito = request.user.carrito_compras.id
    productos = Carrito_Compras_Producto.objects.filter(carrito=carrito)
    for p in productos:
        p.producto.cantidad_disponible = p.producto.cantidad_disponible - p.cantidad 
        p.producto.save()
    productos.delete()
    """
    return render(request, 'ventas/pago.html', {'factura': pk})

def confirmar_pago(request):
    datos = request.POST
  
    factura = Factura.objects.filter(id=datos['factura']).first()
    factura.estado = True
    factura.save()
    carrito = request.user.carrito_compras.id
    productos = Carrito_Compras_Producto.objects.filter(carrito=carrito)
    for p in productos:
        p.producto.cantidad_disponible = p.producto.cantidad_disponible - p.cantidad 
        p.producto.save()
    productos.delete()

    m = 0

    if 'metodo_0' in datos:
        m = m + 1
    if 'metodo_1' in datos:
        m = m + 1
    if 'metodo_2' in datos:
        m = m + 1
    if m == 1:
        if datos['metodo_0'] == 'Efectivo':
            Factura_Pago(factura=factura, metodo_pago=datos['metodo_0'], valor=factura.total).save()
        elif datos['metodo_0'] == 'Tarjeta Crédito':
            f = Factura_Pago(factura=factura, metodo_pago=datos['metodo_0'], valor=factura.total)
            f.save()
            if TarjetaC.objects.filter(numero=datos['numero_0']).exists():
                t = TarjetaC.objects.filter(numero=datos['numero_0']).first()
                t.factura_pago.add(f)
            else:
                t = TarjetaC(numero=datos['numero_0'], fecha=datos['fecha_0'], franquicia=datos['franqui_0'], cvv=datos['cvv_0'], cuotas=datos['cuota_0'])
                t.save()
                t.factura_pago.add(f)
        elif datos['metodo_0'] == 'Tarjeta Débito':
            f = Factura_Pago(factura=factura, metodo_pago=datos['metodo_0'], valor=factura.total)
            f.save()
            if TarjetaD.objects.filter(numero=datos['numero_0']).exists():
                t = TarjetaD.objects.filter(numero=datos['numero_0']).first()
                t.factura_pago.add(f)
            else:
                t = TarjetaD(numero=datos['numero_0'], fecha=datos['fecha_0'], banco=datos['banco_0'])
                t.save()
                t.factura_pago.add(f)
    elif m == 2:
        if datos['metodo_0'] == 'Efectivo' and datos['metodo_1'] == 'Efectivo':
            Factura_Pago(metodo_pago=datos['metodo_0'], valor=factura.total, factura=factura).save()
        else:
            for i in range(2):
                metodo = 'metodo_'+str(i) 
                porcentaje = 'porcentaje_'+str(i)
                numero = 'numero_'+str(i)
                fecha = 'fecha_'+str(i)
                banco = 'banco_'+str(i)
                franquicia = 'franqui_'+str(i)
                cvv = 'cvv_'+str(i)
                cuotas = 'cuota_'+str(i)
                valor = factura.total*int(datos[porcentaje])/100

                if datos[metodo] == 'Efectivo':
                    
                    Factura_Pago(factura=factura, metodo_pago=datos[metodo], valor=valor).save()

                elif datos[metodo] == 'Tarjeta Crédito':
                    f = Factura_Pago(factura=factura, metodo_pago=datos[metodo], valor=valor)
                    f.save()
                    if TarjetaC.objects.filter(numero=datos[numero]).exists():
                        t = TarjetaC.objects.filter(numero=datos[numero]).first()
                        t.factura_pago.add(f)
                    else:    
                        t = TarjetaC(numero=datos[numero], fecha=datos[fecha], franquicia=datos[franquicia], cvv=datos[cvv], cuotas=datos[cuotas])
                        t.save()
                        t.factura_pago.add(f)

                elif datos[metodo] == 'Tarjeta Débito':
                    f = Factura_Pago(factura=factura, metodo_pago=datos[metodo], valor=valor)
                    f.save()
                    if TarjetaD.objects.filter(numero=datos[numero]).exists():
                        t = TarjetaD.objects.filter(numero=datos[numero]).first()
                        t.factura_pago.add(f)
                    else:
                        t = TarjetaD(numero=datos[numero], fecha=datos[fecha], banco=datos[banco])
                        t.save()
                        t.factura_pago.add(f)   
    elif m == 3:
        ultimo = 3
        if datos['metodo_0'] == 'Efectivo' and datos['metodo_1'] == 'Efectivo' and datos['metodo_2'] == 'Efectivo':
            Factura_Pago(factura=factura, metodo_pago=datos['metodo_0'], valor=factura.total).save()
        elif datos['metodo_0'] == 'Efectivo' and datos['metodo_1'] == 'Efectivo':
            ultimo = 2
            x = (factura.total*int(datos['porcentaje_0'])/100) + (factura.total*int(datos['porcentaje_1'])/100)
            Factura_Pago(factura=factura, metodo_pago=datos['metodo_0'], valor=x).save()
        elif datos['metodo_0'] == 'Efectivo' and datos['metodo_2'] == 'Efectivo':
            ultimo = 1
            x = (factura.total*int(datos['porcentaje_0'])/100) + (factura.total*int(datos['porcentaje_2'])/100)
            Factura_Pago(factura=factura, metodo_pago=datos['metodo_0'], valor=x).save()
        elif datos['metodo_1'] == 'Efectivo' and datos['metodo_2'] == 'Efectivo':
            ultimo = 0
            x = (factura.total*int(datos['porcentaje_1'])/100) + (factura.total*int(datos['porcentaje_2'])/100)
            Factura_Pago(factura=factura, metodo_pago=datos['metodo_0'], valor=x).save()
        if ultimo == 3:
            for i in range(3):
                metodo = 'metodo_'+str(i) 
                porcentaje = 'porcentaje_'+str(i)
                numero = 'numero_'+str(i)
                fecha = 'fecha_'+str(i)
                banco = 'banco_'+str(i)
                franquicia = 'franqui_'+str(i)
                cvv = 'cvv_'+str(i)
                cuotas = 'cuota_'+str(i)
                valor = factura.total*int(datos[porcentaje])/100

                if datos[metodo] == 'Efectivo':
                    
                    Factura_Pago(factura=factura, metodo_pago=datos[metodo], valor=valor).save()

                elif datos[metodo] == 'Tarjeta Crédito':
                    f = Factura_Pago(factura=factura, metodo_pago=datos[metodo], valor=valor)
                    f.save()
                    if TarjetaC.objects.filter(numero=datos[numero]).exists():
                        t = TarjetaC.objects.filter(numero=datos[numero]).first()
                        t.factura_pago.add(f)
                    else:    
                        t = TarjetaC(numero=datos[numero], fecha=datos[fecha], franquicia=datos[franquicia], cvv=datos[cvv], cuotas=datos[cuotas])
                        t.save()
                        t.factura_pago.add(f)

                elif datos[metodo] == 'Tarjeta Débito':
                    f = Factura_Pago(factura=factura, metodo_pago=datos[metodo], valor=valor)
                    f.save()
                    if TarjetaD.objects.filter(numero=datos[numero]).exists():
                        t = TarjetaD.objects.filter(numero=datos[numero]).first()
                        t.factura_pago.add(f)
                    else:
                        t = TarjetaD(numero=datos[numero], fecha=datos[fecha], banco=datos[banco])
                        t.save()
                        t.factura_pago.add(f)
        else:

            metodo = 'metodo_'+str(ultimo) 
            porcentaje = 'porcentaje_'+str(ultimo)
            numero = 'numero_'+str(ultimo)
            fecha = 'fecha_'+str(ultimo)
            banco = 'banco_'+str(ultimo)
            franquicia = 'franqui_'+str(ultimo)
            cvv = 'cvv_'+str(ultimo)
            cuotas = 'cuota_'+str(ultimo)
            valor = factura.total*int(datos[porcentaje])/100

            if datos[metodo] == 'Tarjeta Débito':
                f = Factura_Pago(factura=factura, metodo_pago=datos[metodo], valor=valor)
                f.save()
                if TarjetaD.objects.filter(numero=datos[numero]).exists():
                    t = TarjetaD.objects.filter(numero=datos[numero]).first()
                    t.factura_pago.add(f)
                else:
                    t = TarjetaD(numero=datos[numero], fecha=datos[fecha], banco=datos[banco])
                    t.save()
                    t.factura_pago.add(f)

            elif datos[metodo] == 'Tarjeta Crédito': 
                f = Factura_Pago(factura=factura, metodo_pago=datos[metodo], valor=valor)
                f.save()
                if TarjetaC.objects.filter(numero=datos[numero]).exists():
                    t = TarjetaC.objects.filter(numero=datos[numero]).first()
                    t.factura_pago.add(f)
                else:    
                    t = TarjetaC(numero=datos[numero], fecha=datos[fecha], franquicia=datos[franquicia], cvv=datos[cvv], cuotas=datos[cuotas])
                    t.save()
                    t.factura_pago.add(f)

    pagos = Factura_Pago.objects.filter(factura=factura)
    tarjetasc = [] 
    tarjetasd = []

    for p in pagos:
        if p.metodo_pago == 'Tarjeta Crédito':
            tarjetasc.append(p.tarjetac_set.all())
        elif p.metodo_pago == 'Tarjeta Débito':
            tarjetasd.append(p.tarjetad_set.all())
   
    pro = Factura_Producto.objects.filter(factura=factura)

    t = 0

    for p in pro:
        t = t + p.subtotal

    iva = (t * 19)/100
    context = {
        'pagos': pagos,
        'factura': factura,
        'carritop': pro,
        'iva': iva,
        'total': t
    }
    messages.success(request, 'Compra realizada con exito!')
    return render(request, 'ventas/factura_final.html', context)

def historial_compras(request, pk):
    usuario = Usuario.objects.get(id=pk)
    facturas = Factura.objects.filter(id_usuario=usuario.id, estado=True)
    iva = []
    total = 0
    for f in facturas:
        productos = Factura_Producto.objects.filter(factura=f)
        for p in productos:
            total = total + p.subtotal
        iva.append((total*19)/100)
        total = 0
    productos = Factura_Producto.objects.all()
    

    return render(request, 'ventas/historial_compras.html', {'facturas': facturas})



            





 
    