from django.contrib.auth.models import User
from gestion_inmuebles.models import Region, Comuna, TipoInmueble, Inmueble

# a. Crear 
def crear_inmueble(nombre, descripcion, m2_construidos, m2_totales, estacionamientos, 
                   habitaciones, banos, direccion, precio_mensual, comuna_id, tipo_inmueble_id, propietario_id):
    comuna = Comuna.objects.get(id=comuna_id)
    tipo = TipoInmueble.objects.get(id=tipo_inmueble_id)
    propietario = User.objects.get(id=propietario_id)

    inmueble = Inmueble.objects.create(
        nombre=nombre,
        descripcion=descripcion,
        m2_construidos=m2_construidos,
        m2_totales=m2_totales,
        estacionamientos=estacionamientos,
        habitaciones=habitaciones,
        banos=banos,
        direccion=direccion,
        precio_mensual=precio_mensual,
        comuna=comuna,
        tipo_inmueble=tipo,
        propietario=propietario
    )
    return inmueble


# b. Listar / Consultar
def listar_inmuebles():
    return Inmueble.objects.all()


# c. Actualizar
def actualizar_inmueble(inmueble_id, nuevo_precio=None, nueva_descripcion=None):
    inmueble = Inmueble.objects.get(id=inmueble_id)
    if nuevo_precio is not None:
        inmueble.precio_mensual = nuevo_precio
    if nueva_descripcion is not None:
        inmueble.descripcion = nueva_descripcion
    inmueble.save()
    return inmueble


# d. Borrar
def borrar_inmueble(inmueble_id):
    inmueble = Inmueble.objects.get(id=inmueble_id)
    inmueble.delete()
    return True