from django import forms
from apps.usuarios.models import Usuario
from .models import Factura_Pago


class Confirmar_Datos(forms.Form):
    nombres = forms.CharField()
    apellidos = forms.CharField()
    direccion = forms.CharField()
    telefono = forms.CharField()
    ciudad = forms.CharField()

class F_Factura_Pago(forms.ModelForm):
    class Meta:
        model =  Factura_Pago
        fields = ['metodo_pago', 'valor']