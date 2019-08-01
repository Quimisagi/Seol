from django.shortcuts import render, redirect, get_object_or_404, render_to_response
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .forms import ProductCreateForm,CategoriaCreateForm,SubcategoriaCreateForm, DetalleCreateForm, ProductUpdateForm, CategoryUpdateForm, SubcategoryUpdateForm
from .models import Categoria, Subcategoria, Producto, Detalle
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.views.generic import DeleteView
from django.forms import modelformset_factory

def productRegister(request):
    if request.method == 'POST':
        form = ProductCreateForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            messages.success(request, 'Producto agregado!')
            return redirect('home')
        else:
            messages.error(request, 'Error!')
            return render(request, 'productos/registrar-producto.html', {'form': form})
    else:
        form = ProductCreateForm()
    return render(request, 'productos/registrar-producto.html', {'form': form})

def menuProductos(request):
    return render(request, 'productos/menu-productos.html', {})

def menuCategorias(request):
    return render(request, 'productos/menu-categorias.html', {})


def categoryRegister(request):


    subcategoria_formset = modelformset_factory(Subcategoria, form=SubcategoriaCreateForm, min_num=1,
     extra=0)
    formset = subcategoria_formset(queryset=Subcategoria.objects.none())

    if request.method == 'POST':
        form1 = CategoriaCreateForm(request.POST)
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

            return redirect('home')
    else:
        form1 = CategoriaCreateForm()
    return render(request, 'productos/registrar-categoria.html', {'form': form1, 'formset': formset})

def productUpdate(request, pk):
    producto = get_object_or_404(Producto, pk=pk)
    if request.method == 'POST':

        form = ProductUpdateForm(request.POST, request.FILES, instance=producto)

        if form.is_valid():
            form.save()
            messages.success(request, 'Producto actualizado!')
            return redirect('lista_producto')
    else:
        form = ProductUpdateForm(instance=producto)

    return render(request, 'productos/actualizar-producto.html', {'form': form, 'producto': producto})

def productList(request):
    context = {
        'productos': Producto.objects.filter(estado=True),
    }
    return render(request, 'productos/lista-producto.html', context)

def categoryList(request):
    context = {
        'categorias': Categoria.objects.filter(estado=True),
        'subcategorias': Subcategoria.objects.filter(estado=True),
    }
    return render(request, 'productos/lista-categoria.html', context)

class ProductDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Producto
    success_url = '/producto/lista'

    def test_func(self, *args, **kwargs):
        producto = get_object_or_404(Producto, pk=self.kwargs['pk'])
        if self.request.method == 'POST':
            producto.estado = False
            producto.save()
            messages.success(self.request, 'Producto eliminado!')
            return redirect('lista_producto')
        else:
            return render(self.request, 'productos/producto_confirm_delete.html', {})

class CategoryDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Categoria
    success_url = '/categoria/lista'

    def test_func(self, *args, **kwargs):
        categoria = get_object_or_404(Categoria, pk=self.kwargs['pk'])
        cat_id = categoria.id
        subcategorias = Subcategoria.objects.filter(categoria_id=cat_id)
        if self.request.method == 'POST':
            categoria.estado = False
            categoria.save()
            for sc in subcategorias:
                sc.estado = False
                sc.save()
            messages.success(self.request, 'Categoria eliminada!')
            return redirect('lista_categoria')
        else:
            return render(self.request, 'productos/categoria_confirm_delete.html', {})

def categoryUpdate(request, pk):

    categoria = get_object_or_404(Categoria, pk=pk)

    if request.method == 'POST':
        form = CategoryUpdateForm(request.POST, instance=categoria)
        if form.is_valid():
            form.save()
            messages.success(request, 'Categoria actualizada!')
            return redirect('lista_categoria')
    else:
        form = CategoryUpdateForm(instance=categoria)
    


    return render(request, 'productos/actualizar-categoria.html', {'form': form, 'categoria': pk})

def subcategoryList(request, pk):
    context = {
        'categoria': Categoria.objects.filter(id=pk).first(),
        'subcategorias': Subcategoria.objects.filter(categoria=pk),
    }

    print(context['categoria'])

    return render(request, 'productos/lista-subcategoria.html', context)


def subcategoryUpdate(request, pk):

    subcategoria = get_object_or_404(Subcategoria, pk=pk)

    if request.method == 'POST':
        form = SubcategoryUpdateForm(request.POST, instance=subcategoria)
        if form.is_valid():
            form.save()
            categoria = subcategoria.categoria
            messages.success(request, 'Subcategoria actualizada!')
            return redirect(subcategoryList, categoria.id)
    else:
        form = SubcategoryUpdateForm(instance=subcategoria)
    
    return render(request, 'productos/actualizar-subcategoria.html', {'form': form})





    
        





            

