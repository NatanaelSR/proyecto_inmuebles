import os
import django
import json

# Configurar el entorno de Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'proyecto_inmuebles.settings')
django.setup()

from django.contrib.auth.models import User
from django.contrib.auth.hashers import make_password
from gestion_inmuebles.models import Perfil

# Datos con los nombres exactos de grupo y tipo de perfil
datos = [
    ("arrendador_carlos", "Carlos", "Soto", "carlos.soto@example.com", "arrendador", 2, 1),
    ("arrendador_ana", "Ana", "Torres", "ana.torres@example.com", "arrendador", 3, 2),
    ("arrendador_luis", "Luis", "Pérez", "luis.perez@example.com", "arrendador", 4, 3),
    ("arrendadora_marta", "Marta", "Gómez", "marta.gomez@example.com", "arrendador", 5, 4),
    ("arrendador_pedro", "Pedro", "Rojas", "pedro.rojas@example.com", "arrendador", 6, 5),
    ("arrendatario_sofia", "Sofía", "Valdés", "sofia.valdes@example.com", "arrendatario", 7, 6),
    ("arrendatario_diego", "Diego", "Silva", "diego.silva@example.com", "arrendatario", 8, 7),
    ("arrendataria_valentina", "Valentina", "Muñoz", "valentina.munoz@example.com", "arrendatario", 9, 8),
    ("arrendatario_ignacio", "Ignacio", "Morales", "ignacio.morales@example.com", "arrendatario", 10, 9),
    ("arrendataria_camila", "Camila", "Herrera", "camila.herrera@example.com", "arrendatario", 11, 10),
]

fixture_list = []
password_hash = make_password("123456")  # Genera el hash real y válido de Django para "123456"

for username, first_name, last_name, email, tipo, user_pk, perfil_pk in datos:
    # 1. Objeto User de Auth
    fixture_list.append({
        "model": "auth.user",
        "pk": user_pk,
        "fields": {
            "password": password_hash,
            "is_superuser": False,
            "username": username,
            "first_name": first_name,
            "last_name": last_name,
            "email": email,
            "is_staff": False,
            "is_active": True,
            "date_joined": "2026-09-01T00:00:00Z",
            "groups": [1 if tipo == "arrendador" else 2] 
        }
    })
    # 2. Objeto Perfil vinculado
    fixture_list.append({
        "model": "gestion_inmuebles.perfil",
        "pk": perfil_pk,
        "fields": {
            "usuario": user_pk,
            "tipo_usuario": tipo
        }
    })

# Asegurar que exista la carpeta fixtures dentro de gestion_inmuebles
os.makedirs("gestion_inmuebles/fixtures", exist_ok=True)
ruta_json = "gestion_inmuebles/fixtures/usuarios.json"

with open(ruta_json, "w", encoding="utf-8") as f:
    json.dump(fixture_list, f, indent=2, ensure_ascii=False)

print(f"¡Archivo '{ruta_json}' generado con éxito!")