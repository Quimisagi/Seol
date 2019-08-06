from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.urls import reverse_lazy
from django.contrib import messages
from .forms import Formulario_Registro_Producto, Formulario_Editar_Producto, Formulario_Registro_Subcategoria, Formulario_Registro_Categoria, Formulario_Editar_Categoria, Formulario_Editar_Subcategoria, Formulario_Registro_Descuento, Formulario_Editar_Descuento
from .models import Categoria, Subcategoria, Producto, Descuento_Producto
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.views.generic import DeleteView
from django.forms import modelformset_factory
from django.core.exceptions import *

#Productos--------------------------------------------------------------------

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

def menu_productos(request):
    return render(request, 'productos/menu-productos.html', {})

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

def lista_producto(request):
    context = {
        'productos': Producto.objects.filter(estado=True),
    }
    return render(request, 'productos/lista-producto.html', context)

class eliminar_producto(LoginRequiredMixin, DeleteView):
    model = Producto
    success_url = reverse_lazy('productos:lista_producto')

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

   
#Categorias--------------------------------------------------------------------------------------------

def menu_categorias(request):
    return render(request, 'productos/menu-categorias.html', {})

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



def lista_categoria(request):
    context = {
        'categorias': Categoria.objects.filter(estado=True),
        'subcategorias': Subcategoria.objects.filter(estado=True),
    }
    return render(request, 'productos/lista-categoria.html', context)



class eliminar_categoria(LoginRequiredMixin, DeleteView):
    model = Categoria
    success_url = reverse_lazy('productos:lista_categoria')

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

def lista_subcategoria(request, pk):
    context = {
        'categoria': Categoria.objects.filter(id=pk).first(),
        'subcategorias': Subcategoria.objects.filter(categoria=pk, estado=True),
    }

    return render(request, 'productos/lista-subcategoria.html', context)


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

class eliminar_subcategoria(LoginRequiredMixin, DeleteView):

    model = Subcategoria

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

def agregar_descuento(request, pk):

    if request.method == 'POST':

        producto = get_object_or_404(Producto, pk=pk)
        
        form = Formulario_Registro_Descuento(request.POST)

        if form.is_valid():

            a = form.save(commit=False)
            a.producto = producto
            a.save()
            messages.success(request, 'Descuento agregado!')
            return redirect('home:home')
    else:
        form = Formulario_Registro_Descuento()
    return render(request, 'productos/registrar-descuento.html', {'form': form})    

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

def lista_descuento(request):
    context = {
        'descuentos': Descuento_Producto.objects.all(),
    }

    return render(request, 'productos/lista-descuento.html', context)


class eliminar_descuento(LoginRequiredMixin, DeleteView):

    model = Descuento_Producto

    success_url = reverse_lazy('productos:lista_descuento')

   

        





            

