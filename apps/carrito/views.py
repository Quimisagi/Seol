from django.shortcuts import render, redirect, get_object_or_404
from .models import Carrito_Compras, Carrito_Compras_Producto
from django.contrib import messages
from apps.productos.models import Producto
from django.contrib.auth.decorators import login_required

def carrito(request):
    carrito = request.user.carrito_compras.id
    productos = Carrito_Compras_Producto.objects.filter(carrito=carrito)
    total = 0
    for producto in productos:
        total = total + producto.subtotal
    iva = (total * 19)/100
    totaliva = total + iva
    context = {
        'carrito': Carrito_Compras.objects.get(id=carrito),
        'carritop': Carrito_Compras_Producto.objects.filter(carrito=carrito),
        'total': total,
        'totaliva': totaliva,
        'iva': iva
    }

    return render(request, 'carrito/carrito-compras.html', context)

@login_required
def agregar_carrito(request, pk, cn):
    producto = get_object_or_404(Producto, pk=pk)
    carro = get_object_or_404(Carrito_Compras, id=request.user.carrito_compras.id)
    carritop = Carrito_Compras_Producto.objects.filter(producto=producto)

    try:
        tiene = False
        for p in carritop:
            if p.carrito == carro:
                tiene = True
                
        #print(tiene)
        if tiene == False:        
            
            if producto.descuento_producto:
                subtotal = producto.precio_venta * cn
                subtotal_dscto = subtotal - (producto.descuento_producto.porcentaje * subtotal)
                Carrito_Compras_Producto(carrito=request.user.carrito_compras, producto=producto, cantidad=cn, subtotal=subtotal_dscto).save()
                messages.success(request, 'Producto agregado al carrito!')
                return redirect('home:home')
            else:
                subtotal = producto.precio_venta * cn
                Carrito_Compras_Producto(carrito=request.user.carrito_compras, producto=producto, cantidad=cn, subtotal=subtotal).save()
                messages.success(request, 'Producto agregado al carrito!')
                return redirect('home:home')
        else:
            
            p = Carrito_Compras_Producto.objects.filter(producto=producto, carrito=carro).first()
            p.cantidad = p.cantidad + cn
            
            if producto.descuento_producto:
                subtotal = producto.precio_venta * p.cantidad
                subtotal_dscto = subtotal - (producto.descuento_producto.porcentaje * subtotal)
                p.subtotal = subtotal_dscto
                p.save()
                messages.success(request, 'Producto agregado al carrito!')
                return redirect('home:home')
            else:
                subtotal = producto.precio_venta * p.cantidad
                p.subtotal = subtotal
                p.save()
                messages.success(request, 'Producto agregado al carrito!')
                return redirect('home:home')

    except:
        tiene = False
        for p in carritop:
            if p.carrito == carro:
                tiene = True
        if tiene == False:        
            
            subtotal = producto.precio_venta * cn
            Carrito_Compras_Producto(carrito=request.user.carrito_compras, producto=producto, cantidad=cn, subtotal=subtotal).save()
            messages.success(request, 'Producto agregado al carrito!')
            return redirect('home:home')
        else:
            
            p = Carrito_Compras_Producto.objects.filter(producto=producto, carrito=carro).first()
            p.cantidad = p.cantidad + cn
            
            subtotal = producto.precio_venta * p.cantidad
            p.subtotal = subtotal
            p.save()
            messages.success(request, 'Producto agregado al carrito!')
            return redirect('home:home')
        

def eliminar_carrito(request, pk):
    
    producto = get_object_or_404(Producto, pk=pk)
    carrito = request.user.carrito_compras.id
    objeto = Carrito_Compras_Producto.objects.filter(producto=producto, carrito=carrito).first()
    objeto.delete()
    messages.success(request, 'Producto eliminado del carrito!')
    return redirect('carrito:carrito')
 

def actualizar_carrito(request, pk, accion):
    producto = get_object_or_404(Producto, pk=pk)
    carro = get_object_or_404(Carrito_Compras, id=request.user.carrito_compras.id)
    carrop = Carrito_Compras_Producto.objects.filter(producto=producto, carrito=carro).first()

    if accion == 1:
        if carrop.cantidad + 1 <= producto.cantidad_disponible:
            carrop.cantidad = carrop.cantidad + 1
            carrop.save()
            try:
                if producto.descuento_producto:
                    subtotal = producto.precio_venta * carrop.cantidad
                    subtotal_dscto = subtotal - (producto.descuento_producto.porcentaje * subtotal)
                    carrop.subtotal = subtotal_dscto
                    carrop.save()
                else:
                    subtotal = producto.precio_venta * carrop.cantidad 
                    carrop.subtotal = subtotal
                    carrop.save()
            except:
                subtotal = producto.precio_venta * carrop.cantidad 
                carrop.subtotal = subtotal
                carrop.save()

            return redirect('carrito:carrito')
        else:
            return redirect('carrito:carrito')
    else:
        if carrop.cantidad > 1:
            carrop.cantidad = carrop.cantidad - 1
            carrop.save()
            try:
                if producto.descuento_producto:
                    subtotal = producto.precio_venta * carrop.cantidad
                    subtotal_dscto = subtotal - (producto.descuento_producto.porcentaje * subtotal)
                    carrop.subtotal = subtotal_dscto
                    carrop.save()
                else:
                    subtotal = producto.precio_venta * carrop.cantidad 
                    carrop.subtotal = subtotal
                    carrop.save()
            except:
                subtotal = producto.precio_venta * carrop.cantidad 
                carrop.subtotal = subtotal
                carrop.save()
            return redirect('carrito:carrito')
        else:
            return redirect('carrito:carrito')





