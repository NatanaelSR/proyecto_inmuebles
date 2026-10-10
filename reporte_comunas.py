import os
import django
from django.db import connection

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'proyecto_inmuebles.settings')
django.setup()

def consultar_inmuebles_por_comuna():
    query = """
        SELECT c.nombre AS comuna, i.nombre, i.descripcion
        FROM gestion_inmuebles_inmueble i
        JOIN gestion_inmuebles_comuna c ON i.comuna_id = c.id
        WHERE i.disponible = TRUE
        ORDER BY c.nombre;
    """
    
    with connection.cursor() as cursor:
        cursor.execute(query)
        resultados = cursor.fetchall()

    ruta_archivo = "reporte_inmuebles_comunas.txt"
    with open(ruta_archivo, "w", encoding="utf-8") as archivo:
        archivo.write("--- LISTADO DE INMUEBLES DISPONIBLES POR COMUNA ---\n\n")
        comuna_actual = ""
        
        for comuna, nombre, descripcion in resultados:
            if comuna != comuna_actual:
                comuna_actual = comuna
                archivo.write(f"\nComuna: {comuna}\n" + "="*40 + "\n")
            archivo.write(f"- Nombre: {nombre}\n  Descripción: {descripcion}\n\n")
            
    print(f"Reporte generado exitosamente en: {ruta_archivo}")

if __name__ == "__main__":
    consultar_inmuebles_por_comuna()