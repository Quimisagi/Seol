from django import forms
from .models import Usuario
from django.contrib.auth.forms import UserCreationForm
from .models import Perfil
from datetime import date

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

    #validacion de fecha nacimiento
    def clean_fecha_nacimiento(self):
        fechaNacimiento = self.cleaned_data.get('fecha_nacimiento')
        if calculateAge(fechaNacimiento) < 18:
            #si es menor de edad
            raise forms.ValidationError("debes ser mayor de 18 años")
        return fechaNacimiento


def calculateAge(birthDate):
    days_in_year = 365.2425
    age = int((date.today() - birthDate).days / days_in_year)
    return age

class Formulario_Editar_Perfil(forms.ModelForm):
    class Meta:
        model = Perfil
        fields = ['imagen']
        widgets = {
            'imagen': forms.FileInput(attrs={'class': 'bootstrap4-multi-input'})
        }


