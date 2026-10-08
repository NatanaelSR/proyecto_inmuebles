# Hito 1 - Conectando Django a una Base de Datos PostgreSQL

Lo siguente corresponde al desarrollo del Hito 1 para la plataforma de arriendo de inmuebles, enfocado en la configuración del entorno, diseño del modelo de datos relacional y manipulación de registros mediante ORM.

---

## 1. Configuración del Entorno de Desarrollo

1.  **Crear y activar entorno virtual:**

    ```bash
    py -m venv env

    .\env\Scripts\activate

    ```

2.  **Instalar dependencias necesarias:**

    ```Bash
    pip install django psycopg2-binary
    ```

3.  **Crear base de datos en PostgreSQL:**

        SQL
        CREATE DATABASE db_inmuebles;

4.  **Configurar settings.py y ejecutar migraciones:**

    Configurar el diccionario DATABASES con el motor django.db.backends.postgresql y las credenciales correspondientes. Luego ejecutar:

        python manage.py makemigrations
        python manage.py migrate

## 2. Modelo Relacional y Claves Foráneas (models.py)

    El modelo representa las entidades del negocio e incluye relaciones relacionales mediante ForeignKey:

    Region: Almacena las regiones del país.

    Comuna: Relacionada con Region (ForeignKey).

    TipoInmueble: Clasificación de la propiedad (Casa, Departamento, Parcela, etc.).

    Inmueble: Modelo principal que contiene los atributos de la propiedad y sus llaves foráneas conectadas a Comuna, TipoInmueble y User (Propietario).

## 3. Operaciones CRUD (gestion_inmuebles/services.py)

    Las 4 operaciones principales del CRUD se encuentran encapsuladas en el archivo de servicios. Para verificar su correcto funcionamiento desde la consola interactiva:

        python manage.py shell

        from gestion_inmuebles.services import crear_inmueble, listar_inmuebles, actualizar_inmueble, borrar_inmueble

        # a. Crear un registro (Create)

        inmueble = crear_inmueble(
        nombre="Departamento Central",
        descripcion="Hermoso departamento de 2 ambientes.",
        m2_construidos=50.0,
        m2_totales=55.0,
        estacionamientos=1,
        habitaciones=2,
        banos=1,
        direccion="Av. Principal 123",
        precio_mensual=450000,
        comuna_id=1,
        tipo_inmueble_id=1,
        propietario_id=1
        )

        # b. Listar registros (Read)

        inmuebles = listar_inmuebles()
        for item in inmuebles:
        print(item.nombre, "-", item.precio_mensual)

        # c. Actualizar un registro (Update)

        actualizar_inmueble(inmueble.id, nuevo_precio=420000, nueva_descripcion="Precio rebajado")

        # d. Borrar un registro (Delete)

        borrar_inmueble(inmueble.id)

# Hito 2 - Parte 1 - Configuración del Admin de Django

Esto corresponde al desarrollo del Hito 2 para la plataforma de arriendo de inmuebles, enfocado en la creación de un superusuario, el registro de modelos en el panel de administración y la personalización de la interfaz para optimizar la gestión de datos mediante columnas, filtros y barras de búsqueda.

---

## 1. Creación del Superusuario

Se crea el super user

1. **Ejecutar el comando de administración:**

   ```bash
   python manage.py createsuperuser
   ```

2. **Ingresar las credenciales solicitadas:**
   - **Usuario:** admin
   - **Email:** admin@ejemplo.com
   - **Contraseña:** **\*\*\*\***

## 2. Registro y Personalización del Admin (gestion_inmuebles/admin.py)

En el archivo admin.py se registraron y personalizaron los modelos `Inmueble`, `Region`, `Comuna` y `TipoInmueble` para mejorar la usabilidad del panel.

    Se importan los modelos al archivo

    Se usa  @admin.register(nombre modelo) para personalizar la visualizacion usando  list_display, search_fields, y list_filter.
