from django import forms
from .models import Usuario
from datetime import date
from django.contrib.auth.forms import UserCreationForm
from .models import Perfil

class Formulario_Registrar_Usuario(UserCreationForm):
   
    class Meta:
        model = Usuario
        fields = ['nombres', 'apellidos', 'password1', 'password2', 'email', 'tipo_documento', 'numero_documento']
        widgets = {
            "numero_documento": forms.NumberInput(),
        }

    def clean_nombres(self):
        dato = self.cleaned_data.get('nombres')
        d = dato.split(" ")
        bandera = True
        for palabra in d:
            if palabra.isalpha():
                pass
            else:
                bandera = False
        if bandera:
            pass
        else:
            raise forms.ValidationError("Digite un nombre válido")
        return d

    def clean_apellidos(self):
        dato = self.cleaned_data.get('apellidos')
        d = dato.split(" ")
        bandera = True
        for palabra in d:
            if palabra.isalpha():
                pass
            else:
                bandera = False
        if bandera:
            pass
        else:
            raise forms.ValidationError("Digite un apellido válido")
        return d


class Formulario_Editar_Usuario(forms.ModelForm):
    nombres = forms.CharField()
    apellidos = forms.CharField()
    email = forms.EmailField()

    class Meta:
        model = Usuario
        fields = ['nombres', 'apellidos', 'email', 'telefono', 'direccion', 'fecha_nacimiento']

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