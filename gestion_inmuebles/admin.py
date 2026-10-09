from django.contrib import admin
from .models import Inmueble, Region, Comuna, TipoInmueble


@admin.register(Inmueble)
class InmuebleAdmin(admin.ModelAdmin):
    # Columnas a mostrar en el listado
    list_display = ('nombre', 'direccion', 'precio_mensual', 'comuna', 'get_region', 'disponible', 'propietario')
    
    #Barra de búsqueda
    search_fields = ('nombre', 'direccion')
    
    # Filtros
    list_filter = ('disponible', 'tipo_inmueble', 'comuna__region', 'comuna')

    # Método para mostrar la Región a través de la Comuna en la tabla list_display
    @admin.display(description='Región')
    def get_region(self, obj):
        return obj.comuna.region.nombre


@admin.register(Region)
class RegionAdmin(admin.ModelAdmin):
    list_display = ('id', 'nombre')
    search_fields = ('nombre',)


@admin.register(Comuna)
class ComunaAdmin(admin.ModelAdmin):
    list_display = ('id', 'nombre', 'region')
    search_fields = ('nombre',)
    list_filter = ('region',)


@admin.register(TipoInmueble)
class TipoInmuebleAdmin(admin.ModelAdmin):
    list_display = ('id', 'nombre')
    search_fields = ('nombre',)