from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login
from django.contrib.auth.models import Group
from .forms import RegistroUsuarioForm, ActualizarUsuarioForm, InmuebleForm
from .models import Perfil, Inmueble
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

# Vista para que el usuario vea y actualice su perfil
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

# Ver oferta de inmuebles disponibles (para Arrendatarios)
@login_required
def listar_inmuebles(request):
    inmuebles = Inmueble.objects.all()
    for inmueble in inmuebles:
        inmueble.precio_formateado = f"{int(inmueble.precio_mensual):,}".replace(",", ".")
        
    return render(request, 'web/lista_inmuebles.html', {'inmuebles': inmuebles})

#Ver detalle de un inmueble específico
@login_required
def detalle_inmueble(request, pk):
    inmueble = get_object_or_404(Inmueble, pk=pk)
    inmueble.precio_formateado = f"{int(inmueble.precio_mensual):,}".replace(",", ".")
    return render(request, 'web/detalle_inmueble.html', {'inmueble': inmueble})


# Vista para que el Arrendador vea SOLO sus inmuebles creados
@login_required
def mis_inmuebles(request):
    if request.user.perfil.tipo_usuario != 'arrendador':
        messages.error(request, 'Acceso denegado: Solo los arrendadores pueden gestionar propiedades.')
        return redirect('home')
    
    inmuebles = Inmueble.objects.filter(propietario=request.user)
    return render(request, 'web/mis_inmuebles.html', {'inmuebles': inmuebles})


# Agregar un nuevo inmueble (solo Arrendadores)
@login_required
def crear_inmueble(request):
    if request.user.perfil.tipo_usuario != 'arrendador':
        messages.error(request, 'Solo los arrendadores pueden publicar inmuebles.')
        return redirect('home')

    if request.method == 'POST':
        form = InmuebleForm(request.POST)
        if form.is_valid():
            inmueble = form.save(commit=False)
            inmueble.propietario = request.user  # Asignamos al usuario autenticado como propietario
            inmueble.save()
            messages.success(request, '¡Inmueble publicado con éxito!')
            return redirect('mis_inmuebles')
    else:
        form = InmuebleForm()

    return render(request, 'web/form_inmueble.html', {'form': form, 'titulo': 'Agregar Nuevo Inmueble'})


# Editar un inmueble existente (solo Arrendador propietario)
@login_required
def editar_inmueble(request, pk):
    inmueble = get_object_or_404(Inmueble, pk=pk, propietario=request.user)

    if request.method == 'POST':
        form = InmuebleForm(request.POST, instance=inmueble)
        if form.is_valid():
            form.save()
            messages.success(request, 'Inmueble actualizado correctamente.')
            return redirect('mis_inmuebles')
    else:
        form = InmuebleForm(instance=inmueble)

    return render(request, 'web/form_inmueble.html', {'form': form, 'titulo': 'Editar Inmueble'})


# Borrar un inmueble (solo Arrendador propietario)
@login_required
def eliminar_inmueble(request, pk):
    inmueble = get_object_or_404(Inmueble, pk=pk, propietario=request.user)
    
    if request.method == 'POST':
        inmueble.delete()
        messages.success(request, 'El inmueble ha sido eliminado.')
        return redirect('mis_inmuebles')

    return render(request, 'web/confirmar_eliminar.html', {'inmueble': inmueble})