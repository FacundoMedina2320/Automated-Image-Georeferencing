Georreferenciación de Imágenes en QGIS
Este proyecto contiene un código diseñado para realizar la georreferenciación de imágenes rasterizadas en QGIS. La georreferenciación es un proceso que alinea una imagen rasterizada con un sistema de coordenadas geográficas conocido, facilitando su integración con otras capas espaciales en un Sistema de Información Geográfica (SIG).

Descripción General
El objetivo de este proyecto es proporcionar una herramienta para alinear imágenes rasterizadas con capas espaciales, permitiendo su uso en análisis y visualización geográfica dentro de QGIS.

Funcionalidades Principales
1. Selección de Capa
ARBA: Permite al usuario seleccionar una capa vectorial y una imagen TIFF para realizar la georreferenciación.
Mapa Mundial: Requiere la selección de una capa del complemento QuickMapServices y una imagen TIFF.
2. Selección de Puntos de Control
Los usuarios pueden seleccionar puntos de control tanto en la capa base como en la imagen TIFF para establecer correspondencias.
Se utiliza QgsMapToolEmitPoint para la selección de puntos, permitiendo a los usuarios capturar coordenadas mediante clics en la interfaz de QGIS.
3. Georreferenciación
La herramienta gdal_translate se emplea para transformar la imagen TIFF según los puntos de control proporcionados.
El resultado es una nueva imagen TIFF georreferenciada, que se guarda como un archivo separado.
4. Advertencia Inicial
Al iniciar el programa, se muestra un mensaje informativo que recuerda al usuario la necesidad de agregar manualmente la capa de "Mapa Mundial" al proyecto antes de ejecutar el proceso de georreferenciación.
Instrucciones de Instalación y Uso
Preparación del Entorno:

Asegúrate de tener QGIS y el complemento QuickMapServices instalados.
Clona este repositorio y abre el proyecto en QGIS.
Selección de Capa Base:

Para ARBA, carga una capa vectorial y selecciona una imagen TIFF.
Para el Mapa Mundial, selecciona una capa a través de QuickMapServices y una imagen TIFF.
Selección de Puntos de Control:

Utiliza la herramienta de selección de puntos para establecer correspondencias entre la capa base y la imagen TIFF.
Georreferenciación:

Ejecuta el proceso de georreferenciación y guarda la imagen transformada.
Contribuciones
Si deseas contribuir a este proyecto, por favor envía una solicitud de extracción (pull request) o reporta problemas (issues) en este repositorio.

Licencia
Este proyecto está bajo la licencia MIT.

Contacto
Para consultas, sugerencias o contribuciones, puedes contactar al autor a través de [tu correo electrónico].
