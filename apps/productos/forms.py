from django import forms
from .models import Producto, Subcategoria, Categoria, Detalle_Producto
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView

class ProductCreateForm(forms.ModelForm):
    class Meta:
        model =  Producto
        fields = ['nombre', 'descripcion', 'precio_venta', 'cantidad_disponible', 'marca', 'subcategoria', 'imagen']

class DetailCreateForm(forms.ModelForm):
    class Meta:
        model = Detalle_Producto
        fields = ['peso', 'color', 'garantia', 'tamano', 'densidad']

class CategoriaCreateForm(forms.ModelForm):
    class Meta:
        model =  Categoria
        fields = ['nombre']

class SubcategoriaCreateForm(forms.ModelForm):
    class Meta:
        model =  Subcategoria
        fields = ['nombre']

class ProductUpdateForm(forms.ModelForm):
    class Meta:
        model = Producto
        fields = ['nombre', 'descripcion', 'precio_venta', 'marca', 'subcategoria', 'imagen']

class CategoryUpdateForm(forms.ModelForm):
    class Meta:
        model = Categoria
        fields = ['nombre']

class SubcategoryUpdateForm(forms.ModelForm):
    class Meta:
        model = Subcategoria
        fields = ['nombre']