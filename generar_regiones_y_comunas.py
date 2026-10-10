import json
import requests
import os

URL = "https://juanbrujo.github.io/chile-regiones-comunas/data/original-simple.json"

NOMBRES_REGIONES = [
    "Arica y Parinacota",
    "Tarapacá",
    "Antofagasta",
    "Atacama",
    "Coquimbo",
    "Valparaíso",
    "Región Metropolitana de Santiago",
    "Libertador General Bernardo O'Higgins",
    "Maule",
    "Ñuble",
    "Biobío",
    "La Araucanía",
    "Los Ríos",
    "Los Lagos",
    "Aysén del General Carlos Ibáñez del Campo",
    "Magallanes y de la Antártica Chilena",
]

NOMBRES_ORIGEN = {
    "Región del Libertador Gral. Bernardo O'Higgins":
        "Libertador General Bernardo O'Higgins",
    "Región del Maule": "Maule",
    "Región de Ñuble": "Ñuble",
    "Región del Biobío": "Biobío",
    "Región de la Araucanía": "La Araucanía",
    "Región de Los Ríos": "Los Ríos",
    "Región de Los Lagos": "Los Lagos",
    "Región Aisén del Gral. Carlos Ibáñez del Campo":
        "Aysén del General Carlos Ibáñez del Campo",
    "Región de Magallanes y de la Antártica Chilena":
        "Magallanes y de la Antártica Chilena",
}

response = requests.get(URL, timeout=30)
response.raise_for_status()
datos = response.json()

# Indexar las comunas por nombre normalizado de región
comunas_por_region = {}

for item in datos["regiones"]:
    nombre = NOMBRES_ORIGEN.get(
        item["region"], item["region"]
    )
    comunas_por_region[nombre] = item["comunas"]

# Construir el fixture en el orden exacto solicitado
fixture = []
ids_region = {}

for pk, nombre in enumerate(NOMBRES_REGIONES, start=1):
    ids_region[nombre] = pk
    fixture.append({
        "model": "gestion_inmuebles.region",
        "pk": pk,
        "fields": {"nombre": nombre},
    })

pk_comuna = 1

for nombre_region in NOMBRES_REGIONES:
    if nombre_region not in comunas_por_region:
        raise ValueError(
            f"No se encontraron comunas para {nombre_region}"
        )

    for nombre_comuna in comunas_por_region[nombre_region]:
        # Ajustes de nombres para mantener consistencia
        if nombre_comuna == "Coihaique":
            nombre_comuna = "Coyhaique"
        elif nombre_comuna == "Aisén":
            nombre_comuna = "Aysén"
        elif nombre_comuna == "Cabo de Hornos (Ex Navarino)":
            nombre_comuna = "Cabo de Hornos"

        fixture.append({
            "model": "gestion_inmuebles.comuna",
            "pk": pk_comuna,
            "fields": {
                "nombre": nombre_comuna,
                "region": ids_region[nombre_region],
            },
        })
        pk_comuna += 1


# Asegurar que exista la carpeta fixtures dentro de gestion_inmuebles
os.makedirs("gestion_inmuebles/fixtures", exist_ok=True)
ruta_json = "gestion_inmuebles/fixtures/regiones_comunas.json"

with open(ruta_json, "w", encoding="utf-8") as f:
    json.dump(fixture, f, ensure_ascii=False, indent=2)

print("Fixture generado correctamente.")
print(f"Regiones: {len(NOMBRES_REGIONES)}")
print(f"Comunas: {pk_comuna - 1}")
print(f"Total de registros: {len(fixture)}")