from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login
from django.contrib.auth.models import Group
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.core.mail import send_mail
from django.utils.html import strip_tags
from django.views.decorators.http import require_POST

from .forms import RegistroUsuarioForm, ActualizarUsuarioForm, InmuebleForm
from .models import Perfil, Inmueble, ImagenInmueble

# Inicio (Home)
def home(request):
    return render(request, 'web/home.html')

# Formulario de registro
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

# Ver y actualizar su perfil
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

# Ver oferta de inmuebles disponibles
def listar_inmuebles(request):
    region_query = request.GET.get('region', '').strip()
    comuna_query = request.GET.get('comuna', '').strip()

    inmuebles = Inmueble.objects.filter(disponible=True)

    if region_query:
        inmuebles = inmuebles.filter(comuna__region__nombre__icontains=region_query)

    if comuna_query:
        inmuebles = inmuebles.filter(comuna__nombre__icontains=comuna_query )

    for inmueble in inmuebles:
        inmueble.precio_formateado = (
            f"{int(inmueble.precio_mensual):,}".replace(",", ".")
        )

    return render(request, 'web/lista_inmuebles.html', {
        'inmuebles': inmuebles,
        'region_query': region_query,
        'comuna_query': comuna_query,
    })

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
        messages.error(
            request,
            'Acceso denegado: Solo los arrendadores pueden gestionar propiedades.'
        )
        return redirect('home')

    region_query = request.GET.get('region', '').strip()
    comuna_query = request.GET.get('comuna', '').strip()
    direccion_query = request.GET.get('direccion', '').strip()

    inmuebles = Inmueble.objects.filter(propietario=request.user )

    if region_query:
        inmuebles = inmuebles.filter(comuna__region__nombre__icontains=region_query)

    if comuna_query:
        inmuebles = inmuebles.filter(comuna__nombre__icontains=comuna_query )

    if direccion_query:
        inmuebles = inmuebles.filter(direccion__icontains=direccion_query)

    for inmueble in inmuebles:
        inmueble.precio_formateado = (
            f"{int(inmueble.precio_mensual):,}".replace(",", ".")
        )

    return render(request, 'web/mis_inmuebles.html', {
        'inmuebles': inmuebles,
        'region_query': region_query,
        'comuna_query': comuna_query,
        'direccion_query': direccion_query,
    })

# Crear un Inmueble (solo para Arrendadores)
@login_required
def crear_inmueble(request):
    if request.user.perfil.tipo_usuario != 'arrendador':
        messages.error(request, 'Solo los arrendadores pueden publicar inmuebles.')
        return redirect('home')

    if request.method == 'POST':
        form = InmuebleForm(request.POST, request.FILES)
        if form.is_valid():
            inmueble = form.save(commit=False)
            inmueble.propietario = request.user # Asignamos el usuario autenticado como propietario
            inmueble.save()

            for imagen in form.cleaned_data['imagenes_adicionales']:
                ImagenInmueble.objects.create(
                    inmueble=inmueble,
                    imagen=imagen
                )

            messages.success(request, '¡Inmueble publicado con éxito!')
            return redirect('mis_inmuebles')
    else:
        form = InmuebleForm()

    return render(request, 'web/form_inmueble.html', {'form': form, 'titulo': 'Agregar Nuevo Inmueble'})

# Editar  un inmueble (solo para Arrendadores)
@login_required
def editar_inmueble(request, pk):
    inmueble = get_object_or_404(Inmueble, pk=pk, propietario=request.user)

    if request.method == 'POST':
        form = InmuebleForm(request.POST, request.FILES, instance=inmueble)
        if form.is_valid():
            form.save()
            
            for imagen in form.cleaned_data['imagenes_adicionales']:
                ImagenInmueble.objects.create(
                    inmueble=inmueble,
                    imagen=imagen
                )

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

# Contactar al Arrendador (solo para Arrendatarios)
@login_required
def contacto_arrendador(request, pk):
    inmueble = get_object_or_404(Inmueble, pk=pk)

    if request.user.perfil.tipo_usuario != 'arrendatario':
        messages.error(
            request,
            'Solo los arrendatarios pueden contactar a los propietarios.'
        )
        return redirect('detalle_inmueble', pk=inmueble.pk)

    propietario = inmueble.propietario

    if request.method == 'POST':
        mensaje = request.POST.get('mensaje', '').strip()

        if not mensaje:
            messages.error(request, 'Debes escribir un mensaje.')
        elif not propietario.email:
            messages.error(
                request,
                'El propietario no tiene un correo registrado.'
            )
        else:
            asunto = f'Nuevo interesado en tu inmueble: {inmueble.nombre}'
            nombre_arrendatario = request.user.get_full_name() or request.user.username
            nombre_propietario = propietario.get_full_name() or propietario.username

            cuerpo_html = f"""
            <h2>Nuevo interesado en tu inmueble</h2>
            <p>Hola {nombre_propietario},</p>
            <p>{nombre_arrendatario} está interesado en tu inmueble.</p>
            <p><strong>Inmueble:</strong> {inmueble.nombre}</p>
            <p><strong>Dirección:</strong> {inmueble.direccion}</p>
            <p><strong>Correo:</strong> {request.user.email or 'No registrado'}</p>
            <h3>Mensaje del interesado</h3>
            <p>{mensaje}</p>
            <p>Este mensaje fue enviado desde la plataforma inmobiliaria.</p>
            """

            cuerpo_texto = strip_tags(cuerpo_html)

            try:
                send_mail(
                    subject=asunto,
                    message=cuerpo_texto,
                    from_email=None,
                    recipient_list=[propietario.email],
                    fail_silently=False,
                    html_message=cuerpo_html,
                )
                messages.success(request, 'Tu mensaje fue enviado al propietario correctamente.')
                return redirect('detalle_inmueble', pk=inmueble.pk)
            
            except Exception as e:
                messages.error(request, 'No se pudo enviar el correo. Inténtalo nuevamente.')

    return render(
        request,
        'web/contacto_arrendador.html',
        {
            'inmueble': inmueble,
            'propietario': propietario,
        }
    )

# Cambiar disponibilidad de un inmueble (solo para Arrendadores)
@login_required
@require_POST
def cambiar_disponibilidad(request, inmueble_id):
    if request.user.perfil.tipo_usuario != 'arrendador':
        messages.error(
            request,
            'Acceso denegado: Solo los arrendadores pueden gestionar propiedades.'
        )
        return redirect('home')

    inmueble = get_object_or_404(
        Inmueble,
        pk=inmueble_id,
        propietario=request.user
    )

    inmueble.disponible = not inmueble.disponible
    inmueble.save(update_fields=['disponible'])

    if inmueble.disponible:
        messages.success(request, 'El inmueble ahora está disponible.')
    else:
        messages.success(request, 'El inmueble se ha marcado como ocupado.')

    return redirect('mis_inmuebles')
