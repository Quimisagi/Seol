from django import forms
from .models import Producto, Subcategoria, Categoria, Descuento_Producto
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

class Formulario_Registro_Descuento(forms.ModelForm):
    class Meta:
        model = Descuento_Producto
        fields = ['fecha_inicio', 'fecha_final', 'porcentaje']

        def clean_porcentaje(self):
            porcentaje = self.cleaned_data.get('porcentaje')
            if porcentaje < 0.1 or porcentaje > 1:
                raise forms.ValidationError("El porcentaje debe ser entre 0.1 y 1")
            return porcentaje

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

class Formulario_Editar_Descuento(forms.ModelForm):
    class Meta:
        model = Descuento_Producto
        fields = ['fecha_inicio', 'fecha_final', 'porcentaje']
