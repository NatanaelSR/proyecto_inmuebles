from django.db import models
from django.contrib.auth.models import User

# Modelo para las Regiones
class Region(models.Model):
    nombre = models.CharField(max_length=100)

    def __str__(self):
        return self.nombre

# Modelo para Comunas
class Comuna(models.Model):
    nombre = models.CharField(max_length=100)
    region = models.ForeignKey(Region, on_delete=models.CASCADE, related_name='comunas')

    def __str__(self):
        return f"{self.nombre} ({self.region.nombre})"

# Modelo para el Tipo de Inmueble 
class TipoInmueble(models.Model):
    nombre = models.CharField(max_length=50)

    def __str__(self):
        return self.nombre

# Modelo Principal
class Inmueble(models.Model):
    nombre = models.CharField(max_length=200)
    descripcion = models.TextField()
    m2_construidos = models.FloatField()
    m2_totales = models.FloatField()
    estacionamientos = models.IntegerField(default=0)
    habitaciones = models.IntegerField(default=1)
    banos = models.IntegerField(default=1)
    direccion = models.CharField(max_length=200)
    precio_mensual = models.DecimalField(max_digits=10, decimal_places=2)
    disponible = models.BooleanField(default=True)

    imagen_principal = models.ImageField(upload_to='inmuebles/principales/', blank=True, null=True)

    # Claves Foráneas 
    comuna = models.ForeignKey(Comuna, on_delete=models.CASCADE, related_name='inmuebles')
    tipo_inmueble = models.ForeignKey(TipoInmueble, on_delete=models.CASCADE, related_name='inmuebles')
    propietario = models.ForeignKey(User, on_delete=models.CASCADE, related_name='inmuebles')

    def __str__(self):
        return f"{self.nombre} - ${self.precio_mensual}"

class ImagenInmueble(models.Model):
    inmueble = models.ForeignKey(Inmueble, related_name='imagenes_carrusel', on_delete=models.CASCADE)
    imagen = models.ImageField(upload_to='inmuebles/carrusel/')

    def __str__(self):
        return f"Imagen para {self.inmueble.nombre}"

TIPO_USUARIO_CHOICES = (
    ('arrendador', 'Arrendador'),
    ('arrendatario', 'Arrendatario'),
)

class Perfil(models.Model):
    usuario = models.OneToOneField(User, on_delete=models.CASCADE, related_name='perfil')
    tipo_usuario = models.CharField(max_length=20, choices=TIPO_USUARIO_CHOICES, default='arrendatario')

    def __str__(self):
        return f"{self.usuario.username} - {self.get_tipo_usuario_display()}"