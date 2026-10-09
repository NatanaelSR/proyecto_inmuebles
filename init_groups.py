import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'proyecto_inmuebles.settings')
django.setup()

from django.contrib.auth.models import Group, Permission
from django.contrib.contenttypes.models import ContentType
from gestion_inmuebles.models import Inmueble

# 1. Crear los 3 grupos
arrendatarios_group, _ = Group.objects.get_or_create(name='Arrendatarios')
arrendadores_group, _ = Group.objects.get_or_create(name='Arrendadores')
administradores_group, _ = Group.objects.get_or_create(name='Administradores')

# 2. Obtener permisos del modelo Inmueble
content_type = ContentType.objects.get_for_model(Inmueble)
perm_add = Permission.objects.get(codename='add_inmueble', content_type=content_type)
perm_change = Permission.objects.get(codename='change_inmueble', content_type=content_type)
perm_delete = Permission.objects.get(codename='delete_inmueble', content_type=content_type)
perm_view = Permission.objects.get(codename='view_inmueble', content_type=content_type)

# 3. Asignar Permisos según el Rol
# Arrendatarios: solo consultar inmuebles
arrendatarios_group.permissions.add(perm_view)

# Arrendadores: agregar, modificar y consultar sus inmuebles
arrendadores_group.permissions.add(perm_add, perm_change, perm_view)

# Administradores: control total (crear, modificar, borrar y consultar)
administradores_group.permissions.add(perm_add, perm_change, perm_delete, perm_view)

print("Los grupos 'Arrendatarios', 'Arrendadores' y 'Administradores' se configuraron con éxito.")