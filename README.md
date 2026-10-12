# Hito 1 - Conectando Django a una Base de Datos PostgreSQL

Lo siguiente corresponde al desarrollo del Hito 1 para la plataforma de arriendo de inmuebles, enfocado en la configuración del entorno, el diseño del modelo de datos relacional y la manipulación de registros mediante ORM.

---

## 1. Configuración del Entorno de Desarrollo

### 1.1. Crear y activar el entorno virtual

```bash
py -m venv env
.\env\Scripts\activate
```

### 1.2. Instalar dependencias

```bash
pip install django psycopg2-binary
```

### 1.3. Crear la base de datos en PostgreSQL

```sql
CREATE DATABASE db_inmuebles;
```

### 1.4. Configurar settings.py y ejecutar migraciones

Configurar el diccionario DATABASES utilizando el motor django.db.backends.postgresql y las credenciales correspondientes.

```bash
python manage.py makemigrations
python manage.py migrate
```

## 2. Modelo Relacional y Claves Foráneas (models.py)

Los modelos representan las entidades del negocio:

- Region: almacena las regiones del país.
- Comuna: relacionada con Region mediante ForeignKey.
- TipoInmueble: clasifica las propiedades (casa, departamento, parcela, etc.).
- Inmueble: contiene los atributos de las propiedades y las claves foráneas hacia Comuna, TipoInmueble y User (propietario).

## 3. Operaciones CRUD (gestion_inmuebles/services.py)

Las cuatro operaciones CRUD se encuentran encapsuladas en el archivo de servicios.

### 3.1. Abrir la consola de Django

```bash
python manage.py shell
```

### 3.2. Importar las funciones

```python
from gestion_inmuebles.services import (
    crear_inmueble,
    listar_inmuebles,
    actualizar_inmueble,
    borrar_inmueble,
)
```

### 3.3. Crear un registro (Create)

```python
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
    propietario_id=1,
)
```

### 3.4. Listar registros (Read)

```python
inmuebles = listar_inmuebles()

for item in inmuebles:
    print(item.nombre, "-", item.precio_mensual)
```

### 3.5. Actualizar un registro (Update)

```python
actualizar_inmueble(
    inmueble.id,
    nuevo_precio=420000,
    nueva_descripcion="Precio rebajado",
)
```

### 3.6. Borrar un registro (Delete)

```python
borrar_inmueble(inmueble.id)
```

---

# Hito 2 - Parte 1 - Configuración del Admin de Django

Este hito contempla la creación de un superusuario, el registro de modelos en el panel de administración y la personalización de la interfaz para optimizar la gestión de datos.

## 1. Creación del Superusuario

### 1.1. Ejecutar el comando

```bash
python manage.py createsuperuser
```

### 1.2. Ingresar las credenciales

- Usuario: admin
- Email: admin@ejemplo.com
- Contraseña: la definida durante la creación.

## 2. Registro y Personalización del Admin (gestion_inmuebles/admin.py)

Se registraron y personalizaron los modelos Inmueble, Region, Comuna y TipoInmueble.

Se utilizaron las siguientes opciones:

- @admin.register(Modelo): registra y personaliza un modelo.
- list_display: define las columnas visibles.
- search_fields: habilita las búsquedas.
- list_filter: permite filtrar registros.

---

# Hito 2 - Parte 2 - Autenticación, Vistas, Plantillas y Control de Acceso

Este hito contempla la autenticación de usuarios mediante Django Auth, la estructuración de plantillas con Bootstrap, la configuración de rutas y la gestión de grupos y permisos.

## 1. Configuración de URLs (urls.py)

En proyecto_inmuebles/urls.py se configuraron las rutas para:

- El panel administrativo.
- La página principal.
- Las vistas de autenticación.
- Las vistas personalizadas.

## 2. Lógica de Vistas (gestion_inmuebles/views.py)

Se implementaron las vistas para la página principal y el registro de usuarios mediante formularios de Django.

## 3. Estructura de Plantillas y Bootstrap (templates/)

Las plantillas se organizaron de la siguiente manera:

```text
templates/
├── base.html
├── includes/
│   └── navbar.html
├── registration/
│   ├── login.html
│   ├── logout.html
│   └── register.html
└── web/
    └── home.html
```

Se integró Bootstrap para el diseño de la interfaz.

## 4. Gestión de Grupos y Permisos (init_groups.py)

Se creó un script para configurar los roles del sistema:

- Arrendador.
- Arrendatario.
- Administrador.

### Ejecución

```bash
python init_groups.py
```

---

# Hito 3 - Población de Base de Datos mediante Fixtures, Gestión de Roles y Reportes SQL

Este hito contempla la carga masiva de datos mediante fixtures, la generación de reportes con consultas SQL y la consolidación de la estructura relacional.

## 1. Población de Datos mediante Fixtures

Se prepararon archivos JSON para cargar los datos iniciales de la aplicación:

- regiones_comunas.json: contiene las regiones y comunas de Chile con sus respectivas relaciones.
- tipos_inmueble.json: contiene las categorías de propiedades disponibles.
- usuarios.json: contiene los usuarios de prueba.
- inmuebles.json: contiene las propiedades asociadas a sus propietarios y comunas.

### Comandos de carga

```bash
python manage.py loaddata regiones_comunas.json
python manage.py loaddata tipos_inmueble.json
python manage.py loaddata usuarios.json
python manage.py loaddata inmuebles.json
```

## 2. Scripts y Reportes por Comuna y Región

Se desarrollaron scripts independientes que utilizan consultas SQL mediante django.db.connection y exportan los resultados a archivos de texto.

### 2.1. Reporte por comuna (reporte_comunas.py)

Realiza un JOIN entre las tablas de inmuebles y comunas para listar las propiedades disponibles por comuna.

Archivo generado: reporte_inmuebles_comunas.txt

### 2.2. Reporte por región (reporte_regiones.py)

Relaciona las tablas de inmuebles, comunas y regiones mediante JOIN para generar un listado de propiedades disponibles por región.

Archivo generado: reporte_inmuebles_regiones.txt

### Ejecución de los reportes

```bash
python reporte_comunas.py
python reporte_regiones.py
```

## 3. Gestión de Roles de Usuario (Arrendador / Arrendatario)

Se implementó un sistema de diferenciación de roles para los usuarios.

### 3.1. Modelo Perfil (models.py)

Se creó un modelo Perfil vinculado al modelo User mediante OneToOneField, con un campo choices para definir si el usuario es arrendador o arrendatario.

### 3.2. Formulario de Registro Personalizado (forms.py)

Se desarrolló RegistroUsuarioForm, heredado de UserCreationForm, para capturar el rol seleccionado durante el registro.

### 3.3. Adaptación de Vistas y Plantillas

Se actualizaron views.py y register.html para procesar el perfil personalizado e integrar la selección de roles en la interfaz.

---

# Hito 4 - Parte 1 - Gestión de Perfiles, Autenticación y Autorización

En esta etapa se implementó el flujo de registro y autenticación de usuarios, vinculando las cuentas con sus perfiles y grupos de permisos de Django.

## 1. Registro Automatizado (views.py)

Se implementaron las siguientes funcionalidades:

- Integración del formulario RegistroUsuarioForm.
- Creación automática del perfil asociado al usuario.
- Captura del tipo de usuario: arrendador o arrendatario.

## 2. Asignación Automática de Grupos de Permisos

Se incorporó la asignación de usuarios a los grupos correspondientes:

- Arrendadores.
- Arrendatarios.

También se agregó manejo de excepciones para evitar errores cuando los grupos no están inicializados.

## 3. Autenticación e Inicio de Sesión Automático

Se implementó login(request, user) después del registro para autenticar automáticamente al usuario.

Luego, se redirige al usuario a la vista perfil_usuario.

## 4. Gestión y Actualización del Perfil

Se implementó una vista protegida mediante login_required para editar los datos personales utilizando ActualizarUsuarioForm.

Las funcionalidades incluyen:

- Modificación del nombre, apellido y correo electrónico.
- Protección del nombre de usuario (username).
- Notificaciones mediante django.contrib.messages.

---

# Hito 4 - Parte 2 - Gestión de Inmuebles, Vistas de Detalle y Formularios

Esta etapa contempla el listado de propiedades, las fichas de detalle y los formularios de creación y edición con Bootstrap.

También se implementó el formato de precios en pesos chilenos (CLP), sin decimales.

## 1. Listado de Inmuebles y Formateo de Moneda

Archivos: views.py y lista_inmuebles.html.

### 1.1. Listado general y listado del propietario

Se implementaron las vistas:

- listar_inmuebles: muestra las propiedades disponibles.
- mis_inmuebles: permite a cada arrendador administrar sus propiedades.

### 1.2. Formateo de precios en CLP

Se utiliza la siguiente expresión para mostrar puntos como separadores de miles:

```python
f"{int(precio_mensual):,}".replace(",", ".")
```

## 2. Ficha de Detalle del Inmueble (detalle_inmueble.html)

Se configuró la vista detalle_inmueble utilizando get_object_or_404 para recuperar una propiedad mediante su identificador (pk).

La plantilla se estructuró en dos columnas con Bootstrap:

- Sección principal: descripción y ubicación del inmueble.
- Panel secundario: precio en CLP y características de la propiedad.

Se muestran las habitaciones, los baños, los estacionamientos y las superficies en metros cuadrados.

## 3. Formularios de Creación y Edición de Inmuebles (form_inmueble.html)

Se desarrollaron formularios basados en ModelForm para registrar y modificar propiedades.

Se utiliza un bucle for field in form para generar dinámicamente los campos.

Se incorporaron las siguientes funcionalidades:

- Clases de Bootstrap, como form-control y form-select.
- Visualización de errores de validación por campo.
- Presentación consistente de los formularios.

# Hito 4 - Parte 3 - Adicionales: Gestión de Imágenes, Búsquedas y Contacto entre Usuarios

## 1. Gestión de Imágenes (Imagen Principal y Carrusel)

Actualización del Modelo de Datos:

- Se incorporó el campo `imagen_principal` en el modelo `Inmueble` para la foto de portada o principal de la propiedad.
- Se creó el modelo relacional `ImagenInmueble` vinculado por llave foránea al inmueble, permitiendo asociar múltiples imágenes adicionales para alimentar la funcionalidad de carrusel en la vista de detalle.

Procesamiento de Archivos Múltiples:

- Se configuraron las vistas de creación (`crear_inmueble`) y edición (`editar_inmueble`) para capturar las cargas múltiples de archivos utilizando `request.FILES.getlist('imagenes_adicionales')`, instanciando y guardando dinámicamente cada registro en `ImagenInmueble`.

Configuración del Formulario y Plantillas:

- Se aseguró el uso correcto del atributo `enctype="multipart/form-data"` en la etiqueta `<form>` de las plantillas HTML para permitir la transferencia binaria de archivos de imagen.
- Se estructuró el input de selección múltiple con el atributo `multiple` para habilitar la selección simultánea de varias fotografías en la interfaz de usuario.
- Se validaron las rutas de almacenamiento local mediante `MEDIA_URL` y `MEDIA_ROOT` para asegurar que las imágenes se guarden y sirvan correctamente desde el servidor de desarrollo.

## 2. Filtros de Búsqueda Avanzados

Integración con el ORM de PostgreSQL y Relaciones de Base de Datos:

- Se utilizaron los parámetros de la URL mediante `request.GET` para capturar los criterios ingresados por los usuarios de forma dinámica.
- Se implementaron consultas estructuradas del ORM utilizando `icontains` (búsqueda insensible a mayúsculas/minúsculas), conectando las tablas mediante relaciones de clave foránea (`comuna__region__nombre` para región y `comuna__nombre` para comuna).

-Vista General de Listado (`listar_inmuebles`):

- Se añadió un formulario de búsqueda que permite a los usuarios filtrar el catálogo completo de propiedades escribiendo el nombre de la **región** o la **comuna**.

Panel de Control del Arrendador (`mis_inmuebles`):

- Se amplió el buscador interno para permitir filtrar el inventario personal combinando tres criterios simultáneamente: **región**, **comuna** y **dirección** específica (`direccion__icontains`).

## 3. Contacto entre Arrendatarios y Arrendadores

Formulario de Contacto:

- Se implementó una vista para que los arrendatarios puedan contactar al propietario desde la ficha de detalle del inmueble.
- Se incorporó un formulario para ingresar el mensaje que se desea enviar al arrendador.

Envío de Correos Electrónicos:

- Se configuró el envío de correos mediante SMTP utilizando el servicio Brevo.
- Se utilizaron variables de entorno en un archivo `.env` para almacenar las credenciales de correo, evitando incluirlas directamente en el código fuente.
- Se implementó el envío de un correo con los datos del inmueble, la información del interesado y el mensaje ingresado.

Validaciones y Notificaciones:

- Se restringió la funcionalidad a usuarios autenticados con perfil de arrendatario.
- Se incorporaron validaciones para comprobar que el mensaje no esté vacío y que el propietario tenga un correo electrónico registrado.
- Se utilizaron `django.contrib.messages` para gestionar las notificaciones de éxito y error.
- Se integró un modal de Bootstrap en la plantilla base para mostrar las notificaciones al usuario.

### 4. Gestión de Disponibilidad de Inmuebles

Se incorporó la funcionalidad para que los arrendadores puedan cambiar el estado de disponibilidad de sus propiedades desde la vista `mis_inmuebles`.

- **Marcar como ocupado:** permite indicar que una propiedad ya fue arrendada o no se encuentra disponible.
- **Marcar como disponible:** permite volver a publicar una propiedad que anteriormente estaba marcada como ocupada.
- **Persistencia en la base de datos:** los cambios se guardan utilizando el campo `disponible` del modelo `Inmueble`.
- **Control de acceso:** únicamente los arrendadores pueden ejecutar esta acción y solo pueden modificar el estado de los inmuebles que les pertenecen.
- **Listado público:** la vista `listar_inmuebles` muestra únicamente los inmuebles cuyo campo `disponible` está establecido en `True`.
- **Administración de propiedades:** los inmuebles ocupados siguen apareciendo en la vista `mis_inmuebles`, permitiendo al arrendador editarlos, eliminarlos o volver a marcarlos como disponibles.
- **Seguridad del formulario:** se utiliza el método POST y el token CSRF para proteger la operación de cambio de estado.

Esta funcionalidad permite mantener actualizado el catálogo público sin eliminar las propiedades de la base de datos y facilita la administración de los inmuebles publicados por cada arrendador.

## Hito 4 - Parte 4 - Adiccionales: Mejoras Visuales y Consistencia de UI/UX

Se implementó una identidad de marca cohesiva y se aplicaron mejoras visuales integrales para elevar la experiencia de usuario y estandarizar la interfaz de la plataforma TuNido.

- Estandarización de Marca e Identidad Visual: Unificación de la paleta corporativa (Azul Marino y Dorado TuNido), tipografía y estados visuales (píldoras, botones y formateo de precios) en todos los formularios y tablas del sistema.

- Refactorización de Interfaz y Formularios (UI): Rediseño limpio de las pantallas de Login, Registro, Gestión de inmuebles y Confirmación de eliminación (con miniatura de propiedad).

- Optimización de Experiencia de Usuario Responsiva (UX): Control de desbordamientos y comportamiento de botones en pantallas móviles para asegurar una navegación fluida sin deformar la maquetación.

---
