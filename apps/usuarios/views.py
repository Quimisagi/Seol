from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .forms import Formulario_Editar_Perfil, Formulario_Editar_Usuario, Formulario_Registrar_Usuario
from django.views.generic import DeleteView
from .models import Usuario
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin

def registrar_usuario(request):
    if request.method == 'POST':
        form = Formulario_Registrar_Usuario(request.POST)
        if form.is_valid():
            a = form.save(commit=False)
            correo = form.cleaned_data.get('email')
            a.username = correo
            a.save()
            messages.success(request, 'Tu cuenta ha sido creada, inicia sesión ahora! ')
            return redirect('home:home')
    else:
        form = Formulario_Registrar_Usuario()
    return render(request, 'usuarios/registrar-usuario.html', {'form': form})
    
@login_required
def editar_perfil(request):
    if request.method == 'POST':
        u_form = Formulario_Editar_Usuario(request.POST, instance=request.user)
        p_form = Formulario_Editar_Perfil(request.POST, request.FILES, instance=request.user.perfil)

        if u_form.is_valid() and p_form.is_valid():
            u_form.save()
            p_form.save()
            messages.success(request, 'Cuenta actualizada!')
            return redirect('usuarios:perfil')

    else:
        u_form = Formulario_Editar_Usuario(instance=request.user)
        p_form = Formulario_Editar_Perfil(instance=request.user.perfil)


    context = {
        'u_form' : u_form,
        'p_form' : p_form
    }
    return render(request, 'usuarios/perfil.html', context)


class eliminar_usuario(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Usuario
    success_url = '/'

    def test_func(self):
        user = self.request.user
        if self.request.method == 'POST':
            user.is_active = False
            user.save()
            messages.success(self.request, 'Cuenta desabilitada!')
            return redirect('home:home')
        else:
            return render(self.request, 'usuarios/usuario_confirm_delete.html', {})
        
