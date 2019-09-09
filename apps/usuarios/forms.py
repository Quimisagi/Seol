from django import forms
from .models import Usuario
from datetime import date
from django.contrib.auth.forms import UserCreationForm
from .models import Perfil

class Formulario_Registrar_Usuario(UserCreationForm):
    nombres = forms.CharField()
    apellidos = forms.CharField()
    email = forms.EmailField()
    #tipo_documento = forms.CharField()
    numero_documento = forms.CharField()
  

    class Meta:
        model = Usuario
        fields = ['nombres', 'apellidos', 'password1', 'password2', 'email', 'tipo_documento', 'numero_documento']

class Formulario_Editar_Usuario(forms.ModelForm):
    nombres = forms.CharField()
    apellidos = forms.CharField()
    email = forms.EmailField()

    class Meta:
        model = Usuario
        fields = ['nombres', 'email', 'apellidos', 'telefono', 'direccion', 'fecha_nacimiento']

    def clean_fecha_nacimiento(self):
            fecha = self.cleaned_data.get('fecha_nacimiento')
            if fecha > date.today() :
                raise forms.ValidationError("Digite una fecha antes de la actual")
            return fecha

class Formulario_Editar_Perfil(forms.ModelForm):
    class Meta:
        model = Perfil
        fields = ['imagen']
        widgets = {
            'imagen': forms.FileInput(attrs={'class': 'bootstrap4-multi-input'})
        }