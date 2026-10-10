from django.shortcuts import render, redirect
from django.contrib.auth import login
from django.contrib.auth.models import Group
from .forms import RegistroUsuarioForm, ActualizarUsuarioForm
from .models import Perfil
from django.contrib.auth.decorators import login_required
from django.contrib import messages


# Vista principal (Home)
def home(request):
    return render(request, 'web/home.html')

# Vista y formulario de registro
def registro(request):
    if request.method == 'POST':
        form = RegistroUsuarioForm(request.POST)
        if form.is_valid():
            user = form.save()
            tipo_usuario = form.cleaned_data.get('tipo_usuario')
            
            if tipo_usuario:
                perfil, created = Perfil.objects.get_or_create(usuario=user)
                perfil.tipo_usuario = tipo_usuario
                perfil.save()
                
                try:
                    grupo = Group.objects.get(name=tipo_usuario)
                    user.groups.add(grupo)
                except Group.DoesNotExist:
                    pass

            login(request, user)
            messages.success(request, '¡Registro exitoso! Bienvenido a tu perfil.')
            return redirect('perfil_usuario')
    else:
        form = RegistroUsuarioForm()
    return render(request, 'registration/register.html', {'form': form})


@login_required
def perfil_usuario(request):
    if request.method == 'POST':
        form = ActualizarUsuarioForm(request.POST, instance=request.user)
        if form.is_valid():
            form.save()
            messages.success(request, 'Tus datos han sido actualizados exitosamente.')
            return redirect('perfil_usuario')
    else:
        form = ActualizarUsuarioForm(instance=request.user)

    return render(request, 'web/perfil.html', {'form': form})