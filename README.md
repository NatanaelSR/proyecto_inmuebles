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

1. El modelo representa las entidades del negocio e incluye relaciones relacionales mediante ForeignKey:

   Region: Almacena las regiones del país.

   Comuna: Relacionada con Region (ForeignKey).

   TipoInmueble: Clasificación de la propiedad (Casa, Departamento, Parcela, etc.).

   Inmueble: Modelo principal que contiene los atributos de la propiedad y sus llaves foráneas conectadas a Comuna, TipoInmueble y User (Propietario).

## 3. Operaciones CRUD (gestion_inmuebles/services.py)

1.  Las 4 operaciones principales del CRUD se encuentran encapsuladas en el archivo de servicios. Para verificar su correcto funcionamiento desde la consola interactiva:

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

1.  Se crea el super user
    1. **Ejecutar el comando de administración:**

    ```bash
       python manage.py createsuperuser
    ```

    2. **Ingresar las credenciales solicitadas:**
       - **Usuario:** admin
       - **Email:** admin@ejemplo.com
       - **Contraseña:** **\*\*\*\***

## 2. Registro y Personalización del Admin (gestion_inmuebles/admin.py)

1.  En el archivo admin.py se registraron y personalizaron los modelos `Inmueble`, `Region`, `Comuna` y `TipoInmueble` para mejorar la usabilidad del panel.

        Se importan los modelos al archivo

        Se usa  @admin.register(nombre modelo) para personalizar la visualizacion usando  list_display, search_fields, y list_filter.

# Hito 2 - Parte 2 - Autenticación, Vistas, Plantillas y Control de Acceso

Lo siguiente corresponde al desarrollo del Hito 2 (Parte 2) para la plataforma de arriendo de inmuebles, enfocado en la implementación de autenticación de usuarios mediante django-auth, estructuración de plantillas con Bootstrap, configuración de rutas y gestión de grupos y permisos.

## 1. Configuración de URLs de Autenticación y Sitio (urls.py)

1. En proyecto_inmuebles/urls.py se actualizaron los archivos de rutas para integrar el panel administrativo, la página principal y las vistas de autenticación nativas y personalizadas.

## 2. Lógica de Vistas (gestion_inmuebles/views.py)

1. En gestion_inmuebles/views.py se implementó la vista para la página principal y el flujo de registro basado en UserCreationForm.

## 3. Estructura de Plantillas y Bootstrap (templates/)

1.  Las plantillas se organizaron bajo una estructura limpia que incluye una plantilla base, componentes reutilizables, vistas de registro/autenticación y la página de inicio, integrando Bootstrap para el diseño base:

    Estructura de directorios:

        templates/
        ├── base.html
        ├── includes/
        │ └── navbar.html
        ├── registration/
        │ ├── login.html
        │ ├── logout.html
        │ └── register.html
        └── web/
        └── home.html

## 4. Gestión de Grupos y Permisos (init_groups.py)

1.  Para cumplir con los requerimientos de control de acceso, se creó un script ejecutable en la raíz del proyecto para poblar los tres roles del sistema (arrendador, arrendatario, y administrador) y asignarles sus permisos sobre el modelo Inmueble:

    Ejecución:

        python init_groups.py

# Hito 3 - Población de Base de Datos mediante Fixtures, Gestión de Roles y Reportes SQL

Lo siguiente corresponde al desarrollo del Hito 3 para la plataforma de arriendo de inmuebles, enfocado en la carga masiva de datos mediante fixtures, la implementación de consultas SQL personalizadas para generación de reportes y la consolidación de la estructura relacional.

## 1. Población de Datos mediante Fixtures (fixtures/)

1. Para asegurar la integridad de la base de datos y poblar el sistema con información inicial de prueba, se estructuraron y cargaron archivos de fixtures en formato JSON en orden de dependencia:

Regiones y Comunas (regiones_comunas.json): Carga masiva de la estructura geográfica oficial de Chile, mapeando correctamente las 16 regiones y sus respectivas comunas con sus llaves foráneas (region_id).

Tipos de Inmueble (tipos_inmueble.json): Definición de las categorías de propiedades disponibles (Casa, Departamento, Parcela, Local Comercial).

Usuarios e Inmuebles (usuarios.json e inmuebles.json): Carga de usuarios de prueba diferenciados y propiedades asociadas a sus respectivos propietarios y comunas reales.

Comandos de carga ejecutados en orden:

    Bash
    python manage.py loaddata regiones_comunas.json
    python manage.py loaddata tipos_inmueble.json
    python manage.py loaddata usuarios.json
    python manage.py loaddata inmuebles.json 2. Reportes SQL y Exportación de Datos

## 2. Scripts y reportes por comuna y region

Para cumplir con los requerimientos de consulta y almacenamiento de información del negocio, se desarrollaron scripts independientes en la raíz del proyecto utilizando consultas SQL directas con django.db.connection para exportar los resultados a archivos de texto:

Reporte por Comuna (reporte_comunas.py): Consulta SQL que realiza un JOIN entre las tablas de inmuebles y comunas para listar las propiedades disponibles agrupadas por comuna, guardando el resultado en reporte_inmuebles_comunas.txt.

Reporte por Región (reporte_regiones.py): Consulta SQL que enlaza inmuebles, comunas y regiones mediante múltiples JOIN para estructurar un listado de inmuebles disponibles ordenados por región, exportándolo a reporte_inmuebles_regiones.txt.

Ejecución de los scripts:

    Bash
    python reporte_comunas.py
    python reporte_regiones.py

## 3. Ampliación del Sistema: Gestión de Roles de Usuario (Arrendador / Arrendatario)

Como mejora complementaria al flujo de registro y control de acceso de la plataforma (fuera del alcance estricto del Hito 3), se implementó un sistema de diferenciación de roles web para los usuarios:

Modelo Perfil (models.py): Creación de un modelo vinculado mediante una relación uno a uno (OneToOneField) al modelo User de Django, incorporando un campo de selección (choices) para definir si el usuario es arrendador o arrendatario.

Formulario de Registro Personalizado (forms.py): Desarrollo de RegistroUsuarioForm (heredado de UserCreationForm) que extiende el registro web estándar para capturar y asignar dinámicamente el rol elegido al crear la cuenta del usuario en la base de datos.

Adaptación de Vistas y Plantillas: Actualización de views.py y del formulario en la interfaz (register.html) para procesar correctamente el perfil personalizado e integrar la selección de roles de forma visual y accesible.
