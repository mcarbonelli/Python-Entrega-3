# Colector de Datos
Aplicación web para recolección de lecturas de medidores eléctricos.

La idea de mi proyecto es que termine siendo una app que pueda ser utilizada por la empresa en donde trabajo. Esta empresa es una distribuidora de eléctrica, y la aplicación que tiene en este momento tiene algunos problemas (algunos de diseño y otros de funcionalidad). Por ejemplo, muestra el estado anterior de un medidor, lo cual no es recomendable ya que el operador podría "Inventar" una lectura actual válida sin ir realemnte a tomar ese regsitro (En mi caso lo muestro, por ahora, para ver que los cálculos y comparaciones se realizan de manera correcta). También tiene problemas de pérdida de información.
También tengo intenciones de incorporar otra app al proyecto que sirva para realizar relevamiento de líneas en baja y media tensión.

## Consigna
Crea una web en Django utilizando Herencia de plantillas, con un modelo de por lo menos 3 clases, un formulario para ingresar datos a las 3 clases y un formulario para buscar algo en la BD, no hace falta que sea sobre las tres clases, con realizar búsqueda sobre una alcanzará.

### Objetivos
Desarrollar tu primer WEB en Django utilizando patrón MVT 
   ---------> La app es una web que utiliza el patrón MVT (tenego models, views y templates)

### Requisitos
- Link de GitHub con el proyecto totalmente subido a la plataforma.
   --------> Se cumple, es este repositorio.

### Proyecto Web Django con patrón MVT que incluya:
- Herencia de HTML. 
   --------> Se cumple, por ejemplo, en models.py cuando cada clase que defino para mi modelo herenda de models (from django.db import models)
- Por lo menos 3 clases en models. 
   --------> Se cumple, por ejemplo, en models.py cuando defino las clases Operador, Cliente y Novedad
- Un formulario para insertar datos a por cada model creado.
   --------> Se cumple parcialmente, por ejemplo, puedo gestionar los tipos de novedad, las rutas, estado. Pero por ahora no puedo gestionar clientes, ni operadores.
- Un formulario para buscar algo en la BD. 
   --------> Se cumple, por ejemplo puedo buscar tipos de novedad, y rutas.
- Un Readme que indique el orden en el que se prueban las cosas y/o donde están las funcionalidades. 
   --------> Se cumple, es este documento.


### Credenciales de Acceso
Como el template que usé de starboostrap (SB Admin) tiene un login, aproveché para investigar un poco el uso de Users y Groups de Django, e intenté integrarlo a mi modelo Operador.  Realcionado con esto también busqué un poco como validar si el usuario de autenticó y puede usar una determinada funcionalidad, (para cuando comencé con el proyecto no habíamos visto los temas de autenticaciones y gestión de usuarios).
Si bien no era un requisito de la consigna, me pareció interesante incorporalos, además me sirve para mi futuro proyecto.

Dejé creado 2 operadores para probar el login/logout y el funcionamiento de la app. 
- **Usuario**: `operador1` | **Contraseña**: `operador123`
- **Usuario**: `operador2` | **Contraseña**: `operador123`


## Funcionalidades

### Autenticación
- Login/Logout de operadores
- Sesiones protegidas

### Dashboard
- Estadísticas sobre la cantidad de rutas y lecturas
- Accesos rápidos a funcionalidades

### Gestión de Periodos
- Selección de año/mes de consumo
- Filtrado automático de rutas

### Rutas
- Listado de rutas
- Estadísticas (total, leídos, faltantes)
- Estados: Abierta/Cerrada
- Acciones: Abrir/Cerrar

### Toma de Lecturas
- Listado de suministros con sus lecturas
- Formularios inline
- Validaciones automáticas
- Cálculo de consumo (kWh)
- Paginación

### Novedades en Suministros
- Novedades predefinidas (checkboxes)
- Observaciones libres (textarea)
- Relación muchos a muchos

### Gestión de Tipos de Novedades
- CRUD de tipos de novedades

### Diseño Mobile-First
- Navegación lateral colapsable
- Botones táctiles grandes
- Responsive en todos los dispositivos


## Estructura del Proyecto
Esta sería la estructura básica del proyecto con las carpetas más relevantes y su decripción

colector_datos/
── colector_datos/     # Es el proyecto principal   
── lecturas/           # Es la app desarrollada (por ahora hay sola una, pero más adelante puede que se agreguen más)
   ── models.py        # Acá se encuentran los modelos que definí y que "migré" a la base de datos
   ── views.py         # Acá se encuentran las vistas que defini utilizando class-based views 
   ── forms.py         # Acá se encuentran los formularios que cree para el ingreso y validacióin de datos 
   ── urls.py          # En esta parte es donde realizo el ruteo de las urls para que vayan a las vistas correspondientes   
   ── templates/       # Esta carpeta están los html que fui crenado para mostrar los datos al usuario, incluyendo el html base que luego heredan los demás html
── startboostrap/      # Carpeta que contiene los archivos CSS, JS, Assets originales descargados (https://startbootstrap.com/theme/sb-admin-pro)
── static/             # Est carpeta  (llamada así por convención) contiene los archivos CSS, JS, Assets que uso el template original
── dblecturas.sqlite3  # Base de datos que contiene las tablas y datos de los modelos mmigrados
── manage.py           # Es el archvio de configuración de django
── README.md           # Este archivo.


## Tecnologías y metodologías utilizadas
- Django
- Python
- HTML5
- CSS3 + Bootstrap 
- JavaScript
- Recurso Descargado: SB Admin Template (https://startbootstrap.com/theme/sb-admin-pro)
- Font Awesome 6
- DataTables
- MTV
- ORM
- Class-Based Views
- SQLite


## Guía de Uso
También dejé una guia en la pantalla principal o home (dashboard)

1. **Login**: Acceder con credenciales de operador
2. **Seleccionar Periodo**: Elegir año/mes (ej: Diciembre 2024 que hay datos)
3. **Ver Rutas**: Listar rutas disponibles con estadísticas
4. **Tomar Lecturas**: 
   - Ingresar lectura actual de cada medidor
   - La app valida y calcula consumo automáticamente
5. **Agregar Novedades**: Opcionalmente se pueden agregar novedades o escribir observaciones
6. **Cerrar Ruta**: Una vez completadas todas las lecturas (mientras esté cerrada no se podrán registrar más lecturas, aunque se puede abrir de nuevo para modificar algo y volver a cerrar)
7. **Mantenimiento de Novedades**: Agregar, modificar o eliminar tipo de novedades

## Validaciones
- Lectura debe ser > 0
- Lectura actual ≥ Lectura anterior
- No se pueden modificar rutas cerradas

## Notas
- El proyecto usa SQLite para desarrollo
- Idioma: Español (Argentina)
- Timezone: America/Argentina/Buenos_Aires
- Diseño optimizado para dispositivos móviles

## Autor
Mauricio G. Carbonelli

## Licencia
Proyecto educativo - Entrega 3 - Carrera de Data Science - Materia: Python - Coderhouse (comisión 87370)
