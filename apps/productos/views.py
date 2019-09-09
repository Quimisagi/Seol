from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required, permission_required
from django.urls import reverse_lazy
from django.contrib import messages
from .forms import Formulario_Registro_Producto, Formulario_Editar_Producto, Formulario_Registro_Subcategoria, Formulario_Registro_Categoria, Formulario_Editar_Categoria, Formulario_Editar_Subcategoria, Formulario_Registro_Descuento, Formulario_Editar_Descuento
from .models import Categoria, Subcategoria, Producto, Descuento_Producto
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin, PermissionRequiredMixin
from django.views.generic import DeleteView
from django.forms import modelformset_factory
from django.core.exceptions import *

#Productos--------------------------------------------------------------------

@permission_required('productos.add_producto', login_url=None, raise_exception=True)
def agregar_producto(request):
    if request.method == 'POST':
        form = Formulario_Registro_Producto(request.POST, request.FILES)

        if form.is_valid():
            form.save()
            messages.success(request, 'Producto agregado!')
            return redirect('home:home')
        else:
            messages.error(request, 'Error!')
            return render(request, 'productos/registrar-producto.html', {'form': form})
    else:
        form = Formulario_Registro_Producto()
    return render(request, 'productos/registrar-producto.html', {'form': form})

@permission_required('productos.view_producto', login_url=None, raise_exception=True)
def menu_productos(request):
    return render(request, 'productos/menu-productos.html', {})

@permission_required('productos.change_producto', login_url=None, raise_exception=True)
def editar_producto(request, pk):
    producto = get_object_or_404(Producto, pk=pk)
    if request.method == 'POST':

        form = Formulario_Editar_Producto(request.POST, request.FILES, instance=producto)

        if form.is_valid():
            form.save()
            messages.success(request, 'Producto actualizado!')
            return redirect('productos:lista_producto')
    else:
        form = Formulario_Editar_Producto(instance=producto)

    return render(request, 'productos/actualizar-producto.html', {'form': form, 'producto': producto})

@permission_required('productos.view_producto', login_url=None, raise_exception=True)
def lista_producto(request):
    context = {
        'productos': Producto.objects.filter(estado=True),
    }
    return render(request, 'productos/lista-producto.html', context)


class eliminar_producto(LoginRequiredMixin, PermissionRequiredMixin, DeleteView):
    model = Producto
    success_url = reverse_lazy('productos:lista_producto')
    permission_required = 'productos.delete_producto'

    
    def delete(self, request, *args, **kwargs):
        """
        Call the delete() method on the fetched object and then redirect to the
        success URL.
        """
        self.object = self.get_object()
        success_url = self.get_success_url()

        self.object.estado = False
        self.object.save()
        messages.success(self.request, 'Producto eliminada!')
        return redirect(success_url)

def detalle_producto(request, pk):
    
    producto = get_object_or_404(Producto, pk=pk)
    
    try:
        if producto.descuento_producto:
            precio_viejo = producto.precio_venta
            producto.precio_venta = (producto.precio_venta) - (producto.precio_venta * producto.descuento_producto.porcentaje)
            producto.descuento_producto.porcentaje = producto.descuento_producto.porcentaje * 100
            return render(request, 'productos/detalle_producto.html', {'producto': producto, 'precio_viejo': precio_viejo})
        else:
            return render(request, 'productos/detalle_producto.html', {'producto': producto})
    except ObjectDoesNotExist:
        return render(request, 'productos/detalle_producto.html', {'producto': producto})

@permission_required('productos.change_producto', login_url=None, raise_exception=True)
def abastecer_producto(request, pk):

    producto = get_object_or_404(Producto, pk=pk)
    cantidad = request.POST['cantidad']
    producto.cantidad_disponible = producto.cantidad_disponible + int(cantidad)
    producto.save()

    return redirect('reportes:reporte_baja_existencia')


   
#Categorias--------------------------------------------------------------------------------------------
@permission_required('productos.view_categoria', login_url=None, raise_exception=True)
def menu_categorias(request):
    return render(request, 'productos/menu-categorias.html', {})

@permission_required('productos.add_categoria', login_url=None, raise_exception=True)
def agregar_categoria(request):
    subcategoria_formset = modelformset_factory(Subcategoria, form=Formulario_Registro_Subcategoria, min_num=1,
     extra=0)
    formset = subcategoria_formset(queryset=Subcategoria.objects.none())

    if request.method == 'POST':
        form1 = Formulario_Registro_Categoria(request.POST)
        formset = subcategoria_formset(request.POST)
        if form1.is_valid() and formset.is_valid():
            form1.save()

            for form in formset:

                nombre_categoria = form1.cleaned_data.get('nombre')
                categoria = Categoria.objects.filter(nombre = nombre_categoria).first()
                
                nombre_subcategoria = form.cleaned_data.get('nombre')
                if categoria and nombre_subcategoria:
                    Subcategoria(nombre=nombre_subcategoria, categoria=categoria).save()

            messages.success(request, 'Categoria agregada!')

            return redirect('home:home')
    else:
        form1 = Formulario_Registro_Categoria()
    return render(request, 'productos/registrar-categoria.html', {'form': form1, 'formset': formset})


@permission_required('productos.view_categoria', login_url=None, raise_exception=True)
def lista_categoria(request):
    context = {
        'categorias': Categoria.objects.filter(estado=True),
        'subcategorias': Subcategoria.objects.filter(estado=True),
    }
    return render(request, 'productos/lista-categoria.html', context)



class eliminar_categoria(LoginRequiredMixin, PermissionRequiredMixin, DeleteView):
    model = Categoria
    success_url = reverse_lazy('productos:lista_categoria')
    permission_required = 'productos.delete_categoria'
    
    def delete(self, request, *args, **kwargs):
        """
        Call the delete() method on the fetched object and then redirect to the
        success URL.
        """
        self.object = self.get_object()
        subcategorias = self.object.subcategorias.all()
        success_url = self.get_success_url()

        self.object.estado = False
        self.object.save()
        for sc in subcategorias:
            sc.estado = False
            sc.save()
        messages.success(self.request, 'Categoria eliminada!')
        return redirect(success_url)
        

@permission_required('productos.change_categoria', login_url=None, raise_exception=True)
def editar_categoria(request, pk):

    categoria = get_object_or_404(Categoria, pk=pk)

    if request.method == 'POST':
        form = Formulario_Editar_Categoria(request.POST, instance=categoria)
        if form.is_valid():
            form.save()
            messages.success(request, 'Categoria actualizada!')
            return redirect('productos:lista_categoria')
    else:
        form = Formulario_Editar_Categoria(instance=categoria)
    return render(request, 'productos/actualizar-categoria.html', {'form': form, 'categoria': pk})

#Subcategoria------------------------------------------------------------------------------------------------
@permission_required('productos.view_subcategoria', login_url=None, raise_exception=True)
def lista_subcategoria(request, pk):
    context = {
        'categoria': Categoria.objects.filter(id=pk).first(),
        'subcategorias': Subcategoria.objects.filter(categoria=pk, estado=True),
    }

    return render(request, 'productos/lista-subcategoria.html', context)

@permission_required('productos.change_subcategoria', login_url=None, raise_exception=True)
def editar_subcategoria(request, pk):

    subcategoria = get_object_or_404(Subcategoria, pk=pk)

    if request.method == 'POST':
        form = Formulario_Editar_Subcategoria(request.POST, instance=subcategoria)
        if form.is_valid():
            form.save()
            categoria = subcategoria.categoria
            messages.success(request, 'Subcategoria actualizada!')
            return redirect('productos:lista_subcategoria', categoria.id)
    else:
        form = Formulario_Editar_Subcategoria(instance=subcategoria)
    return render(request, 'productos/actualizar-subcategoria.html', {'form': form})


class eliminar_subcategoria(LoginRequiredMixin, PermissionRequiredMixin, DeleteView):

    model = Subcategoria
    permission_required = 'productos.delete_subcategoria'
    
    def delete(self, request, *args, **kwargs):
        """
        Call the delete() method on the fetched object and then redirect to the
        success URL.
        """
        self.object = self.get_object()
        categoria = self.object.categoria
       
        self.object.estado = False
        self.object.save()
        messages.success(self.request, 'Subcategoria eliminada!')
        return redirect('productos:lista_subcategoria', categoria.id)

@permission_required('productos.add_subcategoria', login_url=None, raise_exception=True)
def agregar_subcategoria(request, pk):

    if request.method == 'POST':

        categoria = get_object_or_404(Categoria, pk=pk)
        
        form = Formulario_Registro_Subcategoria(request.POST)

        if form.is_valid():

            a = form.save(commit=False)
            a.categoria = categoria
            a.save()
            messages.success(request, 'Subcategoria agregada!')
            return redirect('productos:lista_subcategoria', categoria.id)
    else:
        form = Formulario_Registro_Subcategoria()
    return render(request, 'productos/registrar-subcategoria.html', {'form': form})    


#Descuentos---------------------------------------------------------------------------------------------------------------------
@permission_required('productos.add_descuento_producto', login_url=None, raise_exception=True)
def agregar_descuento(request, pk):

    producto = get_object_or_404(Producto, pk=pk)

    if request.method == 'POST':
        
        fecha1 = request.POST['reservation'].split('-')[0]
        fecha2 = request.POST['reservation'].split('-')[1]
        porcentaje = request.POST['porcentaje']

        fecha_inicio = fecha1.split('/')[0]+'-'+fecha1.split('/')[1]+'-'+fecha1.split('/')[2]
        fecha_final = fecha2.split('/')[0]+'-'+fecha2.split('/')[1]+'-'+fecha2.split('/')[2]

        a = Descuento_Producto(fecha_inicio=fecha_inicio, fecha_final=fecha_final, porcentaje=porcentaje, producto=producto)
        a.save()
        messages.success(request, 'Descuento agregado!')
        return redirect('productos:lista_descuento')
    
    return render(request, 'productos/registrar-descuento.html', {'producto': producto})    

@permission_required('productos.change_descuento_producto', login_url=None, raise_exception=True)
def editar_descuento(request, pk):

    dscto = get_object_or_404(Descuento_Producto, pk=pk)
    
    if request.method == 'POST':
        form = Formulario_Editar_Descuento(request.POST, instance=dscto) 
        if form.is_valid():
            form.save()
            messages.success(request, 'Descuento actualizado!')
            return redirect('productos:lista_descuento')
    else:
        form = Formulario_Editar_Descuento(instance=dscto)
    return render(request, 'productos/actualizar-descuento.html', {'form': form})

@permission_required('productos.view_descuento_producto', login_url=None, raise_exception=True)
def lista_descuento(request):
    context = {
        'descuentos': Descuento_Producto.objects.all(),
    }

    return render(request, 'productos/lista-descuento.html', context)

#@permission_required('productos.delete_descuento_producto', login_url=None, raise_exception=True)
class eliminar_descuento(LoginRequiredMixin, PermissionRequiredMixin, DeleteView):
    permission_required = 'productos.delete_descuento_producto'
    model = Descuento_Producto
    success_url = reverse_lazy('productos:lista_descuento')

   

        





            

