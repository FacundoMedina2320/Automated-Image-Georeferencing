from qgis.core import (
    QgsProject, QgsRasterLayer, QgsVectorLayer, QgsCoordinateReferenceSystem, QgsCoordinateTransform
)
from qgis.gui import QgsMapToolEmitPoint
from PyQt5.QtWidgets import QFileDialog, QMessageBox, QInputDialog
from PyQt5.QtGui import QColor
import subprocess
import os

class PointTool(QgsMapToolEmitPoint):
    def __init__(self, canvas, prompt_message, max_points=4):
        self.canvas = canvas
        self.points = []
        self.prompt_message = prompt_message
        self.max_points = max_points
        QgsMapToolEmitPoint.__init__(self, self.canvas)

    def canvasPressEvent(self, event):
        point = self.toMapCoordinates(event.pos())
        self.points.append(point)
        print(f"Point selected: {point}")
        if len(self.points) == self.max_points:
            QMessageBox.information(None, "Information", self.prompt_message)
            self.deactivate()

    def deactivate(self):
        self.canvas.unsetMapTool(self)
        QgsMapToolEmitPoint.deactivate(self)
        self.deactivated.emit()

def georeferenciar_imagen(imagen_path, puntos_tif, puntos_capa, output_path):
    crs_capa = QgsCoordinateReferenceSystem("EPSG:22185")
    crs_tif = QgsCoordinateReferenceSystem("EPSG:22185")

    transform = QgsCoordinateTransform(crs_tif, crs_capa, QgsProject.instance().transformContext())
    puntos_tif_transformed = [transform.transform(p[0], p[1]) for p in puntos_tif]

    gcp_list = []
    for (ax, ay), (px, py) in zip(puntos_capa, puntos_tif_transformed):
        gcp_list.append(f'-gcp {px} {py} {ax} {ay}')
    
    gdal_translate_command = [
        'gdal_translate',
        '-of', 'GTiff',
        '-a_srs', crs_capa.authid()
    ] + gcp_list + [imagen_path, output_path]
    
    print("Running gdal_translate command:", " ".join(gdal_translate_command))
    try:
        subprocess.run(gdal_translate_command, check=True)
    except subprocess.CalledProcessError as e:
        print(f"Error al ejecutar gdal_translate: {e}")
    
    if os.path.exists(output_path):
        raster_layer = QgsRasterLayer(output_path, "Georreferenciada")
        if raster_layer.isValid():
            QgsProject.instance().addMapLayer(raster_layer)
            print(f"Imagen georreferenciada guardada en {output_path}")
        else:
            print("Error: No se pudo añadir la capa georreferenciada al proyecto.")
    else:
        print("Error: No se pudo crear la imagen georreferenciada.")

def listar_mapas_disponibles():
    layer_names = [layer.name() for layer in QgsProject.instance().mapLayers().values() if isinstance(layer, QgsRasterLayer)]
    return layer_names

def main():
    # Advertencia inicial sobre el mapa mundial
    QMessageBox.information(None, "Advertencia", "Si selecciona 'Mapa Mundial', asegúrese de agregar manualmente la capa del Mapa Mundial al proyecto antes de ejecutar el proceso.")

    layer_choice, ok = QInputDialog.getItem(None, "Seleccionar Capa", "Seleccione la capa a utilizar:", ["ARBA", "Mapa Mundial"], 0, False)
    
    if not ok:
        print("Operación cancelada.")
        return
    
    if layer_choice == "ARBA":
        imagen_path, _ = QFileDialog.getOpenFileName(None, "Seleccione la imagen TIFF", "", "Imágenes (*.tif *.tiff *.jpg *.jpeg *.png)")
        if not imagen_path:
            print("No se seleccionó ninguna imagen. Abortando.")
            return

        output_path, _ = QFileDialog.getSaveFileName(None, "Guardar imagen georreferenciada", "", "GeoTIFF (*.tif)")
        if not output_path:
            print("No se seleccionó ninguna ruta de salida. Abortando.")
            return
        
        arba_path, _ = QFileDialog.getOpenFileName(None, "Seleccione la capa de ARBA", "", "Shapefiles (*.shp)")
        if not arba_path:
            print("No se seleccionó ninguna capa de ARBA. Abortando.")
            return
        
        arba_layer = QgsVectorLayer(arba_path, "ARBA", "ogr")
        if not arba_layer.isValid():
            print("Error: La capa de ARBA no es válida. Abortando.")
            return
        
        QgsProject.instance().addMapLayer(arba_layer)
        
        raster_layer = QgsRasterLayer(imagen_path, "Imagen TIFF")
        if not raster_layer.isValid():
            print("Error: La imagen TIFF no es válida. Abortando.")
            return
        
        QgsProject.instance().addMapLayer(raster_layer)

        view1 = QgsMapCanvas()
        view1.setLayers([arba_layer])
        view1.setCanvasColor(QColor("white"))
        view1.setExtent(arba_layer.extent())
        view1.show()

        view2 = QgsMapCanvas()
        view2.setLayers([raster_layer])
        view2.setCanvasColor(QColor("white"))
        view2.setExtent(raster_layer.extent())
        view2.show()

        point_tool_arba = PointTool(view1, "Seleccione los mismos cuatro puntos en la imagen TIFF.")
        view1.setMapTool(point_tool_arba)
        QMessageBox.information(None, "Información", "Seleccione cuatro puntos en la capa de ARBA.")
        
        while len(point_tool_arba.points) < 4:
            QgsApplication.processEvents()

        puntos_arba = [(p.x(), p.y()) for p in point_tool_arba.points]
        print(f"Puntos seleccionados en la capa de ARBA: {puntos_arba}")
        
        point_tool_tif = PointTool(view2, "Georreferenciando la imagen, por favor espere.")
        view2.setMapTool(point_tool_tif)
        QMessageBox.information(None, "Información", "Seleccione los mismos cuatro puntos en la imagen TIFF.")
        
        while len(point_tool_tif.points) < 4:
            QgsApplication.processEvents()

        puntos_tif = [(p.x(), p.y()) for p in point_tool_tif.points]
        print(f"Puntos seleccionados en la imagen TIFF: {puntos_tif}")
        
        view1.close()
        view2.close()
        
        georeferenciar_imagen(imagen_path, puntos_tif, puntos_arba, output_path)
        print("Proceso de georreferenciación completado.")

        raster_layer_georeferenced = QgsRasterLayer(output_path, "Imagen Georreferenciada")
        if raster_layer_georeferenced.isValid():
            QgsProject.instance().addMapLayer(raster_layer_georeferenced)
            
            canvas = iface.mapCanvas()
            canvas.setExtent(arba_layer.extent())
            canvas.refresh()
        else:
            print("Error: La imagen georreferenciada no es válida.")
    
    elif layer_choice == "Mapa Mundial":
        imagen_path, _ = QFileDialog.getOpenFileName(None, "Seleccione la imagen TIFF", "", "Imágenes (*.tif *.tiff *.jpg *.jpeg *.png)")
        if not imagen_path:
            print("No se seleccionó ninguna imagen. Abortando.")
            return

        output_path, _ = QFileDialog.getSaveFileName(None, "Guardar imagen georreferenciada", "", "GeoTIFF (*.tif)")
        if not output_path:
            print("No se seleccionó ninguna ruta de salida. Abortando.")
            return

        qms_layer_names = listar_mapas_disponibles()
        
        if not qms_layer_names:
            print("No hay capas de QuickMapServices disponibles. Abortando.")
            return
        
        service_name, ok = QInputDialog.getItem(None, "Seleccionar Mapa Mundial", "Seleccione el mapa del complemento QuickMapServices:", qms_layer_names, 0, False)
        
        if not ok or not service_name:
            print("Operación cancelada.")
            return
        
        mapa_mundial_layer = QgsProject.instance().mapLayersByName(service_name)[0]
        if not mapa_mundial_layer:
            print("Error: La capa seleccionada no se encontró en el proyecto.")
            return
        
        QgsProject.instance().addMapLayer(mapa_mundial_layer)
        
        raster_layer = QgsRasterLayer(imagen_path, "Imagen TIFF")
        if not raster_layer.isValid():
            print("Error: La imagen TIFF no es válida. Abortando.")
            return
        
        QgsProject.instance().addMapLayer(raster_layer)

        view1 = QgsMapCanvas()
        view1.setLayers([mapa_mundial_layer])
        view1.setCanvasColor(QColor("white"))
        view1.setExtent(mapa_mundial_layer.extent())
        view1.show()

        view2 = QgsMapCanvas()
        view2.setLayers([raster_layer])
        view2.setCanvasColor(QColor("white"))
        view2.setExtent(raster_layer.extent())
        view2.show()

        point_tool_map = PointTool(view1, "Seleccione los mismos cuatro puntos en la imagen TIFF.")
        view1.setMapTool(point_tool_map)
        QMessageBox.information(None, "Información", "Seleccione cuatro puntos en la capa del Mapa Mundial.")
        
        while len(point_tool_map.points) < 4:
            QgsApplication.processEvents()

        puntos_map = [(p.x(), p.y()) for p in point_tool_map.points]
        print(f"Puntos seleccionados en la capa de Mapa Mundial: {puntos_map}")
        
        point_tool_tif = PointTool(view2, "Georreferenciando la imagen, por favor espere.")
        view2.setMapTool(point_tool_tif)
        QMessageBox.information(None, "Información", "Seleccione los mismos cuatro puntos en la imagen TIFF.")
        
        while len(point_tool_tif.points) < 4:
            QgsApplication.processEvents()

        puntos_tif = [(p.x(), p.y()) for p in point_tool_tif.points]
        print(f"Puntos seleccionados en la imagen TIFF: {puntos_tif}")
        
        view1.close()
        view2.close()
        
        georeferenciar_imagen(imagen_path, puntos_tif, puntos_map, output_path)
        print("Proceso de georreferenciación completado.")

        raster_layer_georeferenced = QgsRasterLayer(output_path, "Imagen Georreferenciada")
        if raster_layer_georeferenced.isValid():
            QgsProject.instance().addMapLayer(raster_layer_georeferenced)
            
            canvas = iface.mapCanvas()
            canvas.setExtent(mapa_mundial_layer.extent())
            canvas.refresh()
        else:
            print("Error: La imagen georreferenciada no es válida.")

# Ejecutar la función principal
main()
