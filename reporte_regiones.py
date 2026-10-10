import os
import django
from django.db import connection

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'proyecto_inmuebles.settings')
django.setup()

def consultar_inmuebles_por_region():
    query = """
        SELECT r.nombre AS region, i.nombre, i.descripcion
        FROM gestion_inmuebles_inmueble i
        JOIN gestion_inmuebles_comuna c ON i.comuna_id = c.id
        JOIN gestion_inmuebles_region r ON c.region_id = r.id
        WHERE i.disponible = TRUE
        ORDER BY r.nombre;
    """
    
    with connection.cursor() as cursor:
        cursor.execute(query)
        resultados = cursor.fetchall()

    ruta_archivo = "reporte_inmuebles_regiones.txt"
    with open(ruta_archivo, "w", encoding="utf-8") as archivo:
        archivo.write("--- LISTADO DE INMUEBLES DISPONIBLES POR REGIÓN ---\n\n")
        region_actual = ""
        
        for region, nombre, descripcion in resultados:
            if region != region_actual:
                region_actual = region
                archivo.write(f"\nRegión: {region}\n" + "="*40 + "\n")
            archivo.write(f"- Nombre: {nombre}\n  Descripción: {descripcion}\n\n")
            
    print(f"Reporte generado exitosamente en: {ruta_archivo}")

if __name__ == "__main__":
    consultar_inmuebles_por_region()