from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .forms import UserRegisterForm,UserUpdateForm,ProfileUpdateForm
from django.views.generic import DeleteView
from .models import Usuario
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin

def register(request):
    if request.method == 'POST':
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            a = form.save(commit=False)
            correo = form.cleaned_data.get('email')
            a.username = correo
            a.save()
            messages.success(request, 'Tu cuenta ha sido creada, loguea ahora! ')
            return redirect('home')
    else:
        form = UserRegisterForm()
    return render(request, 'usuarios/register.html', {'form': form})
    
@login_required
def profile(request):
    if request.method == 'POST':
        u_form = UserUpdateForm(request.POST, instance=request.user)
        p_form = ProfileUpdateForm(request.POST, request.FILES, instance=request.user.perfil)

        if u_form.is_valid() and p_form.is_valid():
            u_form.save()
            p_form.save()
            messages.success(request, 'Cuenta actualizada!')
            return redirect('profile')

    else:
        u_form = UserUpdateForm(instance=request.user)
        p_form = ProfileUpdateForm(instance=request.user.perfil)


    context = {
        'u_form' : u_form,
        'p_form' : p_form
    }
    return render(request, 'usuarios/profile.html', context)


class PostDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Usuario
    success_url = '/'

    def test_func(self):
        user = self.request.user
        if self.request.method == 'POST':
            user.is_active = False
            user.save()
            messages.success(self.request, 'Cuenta desabilitada!')
            return redirect('home')
        else:
            return render(self.request, 'usuarios/usuario_confirm_delete.html', {})
        
