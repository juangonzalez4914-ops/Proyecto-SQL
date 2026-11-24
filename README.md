Sistema Web de Consulta y Analisis de Datos Abiertos de Colombia

Proyecto del tercer corte de la asignatura Desarrollo de Aplicaciones con Acceso a Datos.

Es una aplicacion web hecha con Python y Flask. Consulta una API de datos abiertos de Colombia, guarda los registros en SQL Server y los muestra en una pagina web donde se pueden buscar. Esta organizada con el patron MVC.

Objetivo

Consultar datos abiertos desde una API, guardarlos en una base de datos de SQL Server sin repetirlos y mostrarlos en una pagina web con un buscador y un resumen sencillo.

Datos que se usan

Se usa el conjunto de datos Casos positivos de COVID-19 en Colombia, del portal datos.gov.co. Su identificador es gt2j-8ykr.

La direccion de la API es https://www.datos.gov.co/resource/gt2j-8ykr.json y la aplicacion pide 100 registros ordenados por fecha de reporte, del mas reciente al mas antiguo.

Campos que se guardan

1. id_de_caso se guarda como id_api. Es el identificador del caso y evita que se repitan registros.
2. departamento_nom se guarda como departamento.
3. ciudad_municipio_nom se guarda como municipio.
4. edad se guarda como edad, convertida a numero entero.
5. sexo se guarda como sexo.
6. estado se guarda como estado.
7. recuperado se guarda como recuperado.
8. fecha_reporte_web se guarda como fecha_reporte.
9. Tambien se guarda el registro completo en la columna json_original, por si se necesita algun otro dato despues.

Lo que necesitas para ejecutarlo

Python 3.10 o superior, SQL Server con SQL Server Management Studio y el controlador ODBC Driver 18 for SQL Server.

Como ejecutarlo

1. Abre una terminal en la carpeta del proyecto y crea el entorno virtual con el comando python -m venv venv
2. Activalo con el comando .\venv\Scripts\Activate.ps1
3. Instala las librerias con el comando pip install -r requirements.txt
4. En SQL Server Management Studio abre y ejecuta el archivo script_bd.sql. Este crea la base de datos DatosAbiertosDB y la tabla RegistrosAPI.
5. Copia el archivo .env.example y llamalo .env. Dentro cambia DB_SERVER por el nombre de tu servidor. Si entras a SQL Server con usuario de Windows deja DB_TRUSTED en yes. Si entras con usuario y clave, pon DB_TRUSTED en no y llena DB_USER y DB_PASSWORD.
6. Si quieres probar la API antes, ejecuta python probar_api.py. Esto guarda un ejemplo de la respuesta en la carpeta evidencias.
7. Ejecuta la aplicacion con el comando python app.py
8. Abre en el navegador la direccion http://127.0.0.1:5000
9. Pulsa el boton Consultar API y guardar datos. Si lo pulsas otra vez, no se repiten los registros que ya estan guardados.

Como esta organizado el proyecto

El archivo app.py es el controlador. Recibe lo que pide el usuario, llama a la API y a la base de datos, y elige que pagina mostrar.

La carpeta api tiene el archivo api_client.py, que se encarga de conectarse a la API y traer los datos.

La carpeta models tiene el archivo datos_model.py, que es el modelo. Se conecta a SQL Server, guarda los registros sin repetirlos y hace las consultas.

La carpeta templates tiene el archivo index.html, que es la vista. Muestra el boton, el buscador, el resumen y la tabla.

La carpeta static tiene el archivo estilos.css con los colores y el formato de la pagina.

La carpeta evidencias guarda la respuesta de la API y las capturas de pantalla.

El archivo script_bd.sql crea la base de datos y la tabla. El archivo probar_api.py sirve para probar la API. El archivo requirements.txt tiene las librerias necesarias y el archivo .env.example es el modelo para crear tu archivo .env.

Que puede hacer la aplicacion

Sincronizar. Trae hasta 100 registros de la API y guarda solo los que todavia no estan en la base de datos.

Consultar. Muestra los ultimos 100 registros guardados. Se pueden buscar por municipio, departamento o estado.

Resumen. Muestra el total de registros, la edad promedio, la edad minima, la edad maxima y cuantos casos hay por sexo.

Seguridad

Los datos de conexion estan en el archivo .env, que no se sube a GitHub. Las consultas a la base de datos usan parametros para evitar inyeccion de SQL. El modo debug de Flask se usa solo en el computador local para desarrollo.

Evidencias

En la carpeta evidencias estan la respuesta de la API, una captura de la tabla RegistrosAPI en SQL Server con datos, y capturas de la pagina web mostrando la sincronizacion, la ausencia de repetidos y una busqueda con filtro.


Juan Camilo González Ospino