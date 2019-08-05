from django import forms
from .models import Producto, Subcategoria, Categoria
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView

class Formulario_Registro_Producto(forms.ModelForm):
    class Meta:
        model =  Producto
        fields = ['nombre', 'descripcion', 'precio_venta', 'cantidad_disponible', 'marca', 'subcategoria', 'imagen', 'peso', 'color', 'garantia']

class Formulario_Registro_Categoria(forms.ModelForm):
    class Meta:
        model =  Categoria
        fields = ['nombre']

class Formulario_Registro_Subcategoria(forms.ModelForm):
    class Meta:
        model =  Subcategoria
        fields = ['nombre']

class Formulario_Editar_Producto(forms.ModelForm):
    class Meta:
        model = Producto
        fields = ['nombre', 'descripcion', 'precio_venta', 'marca', 'subcategoria', 'imagen', 'peso', 'color', 'garantia']

class Formulario_Editar_Categoria(forms.ModelForm):
    class Meta:
        model = Categoria
        fields = ['nombre']

class Formulario_Editar_Subcategoria(forms.ModelForm):
    class Meta:
        model = Subcategoria
        fields = ['nombre']