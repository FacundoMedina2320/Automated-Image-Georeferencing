# 🗺️ Georeferencing Images in QGIS

This project provides a tool for **georeferencing raster images** in QGIS, aligning them with known geographic coordinates for integration into a Geographic Information System (GIS).

## 📋 Overview

Georeferencing is the process of associating a raster image with known geographic coordinates. This project offers an efficient way to perform this process in QGIS.

## ⚙️ Key Features

1. **🔍 Base Layer Selection**
   - **ARBA**: Select a vector layer and a TIFF image for georeferencing.
   - **World Map**: Choose a layer from the QuickMapServices plugin and a TIFF image.

2. **📌 Control Points Selection**
   - Select control points on both the base layer and the TIFF image.
   - Use `QgsMapToolEmitPoint` to capture coordinates by clicking in QGIS.

3. **🖼️ Georeferencing Process**
   - Use `gdal_translate` to transform the TIFF image based on the provided control points.
   - Output a new georeferenced TIFF image.

4. **⚠️ Initial Warning**
   - Displays a message reminding the user to manually add the "World Map" layer to the project before starting.

## 🚀 How to Use

1. **Environment Setup**
   - Ensure QGIS and the QuickMapServices plugin are installed.
   - Clone the repository and open the project in QGIS.

2. **🗂️ Load Data**
   - **ARBA**: Load a vector layer and a TIFF image.
   - **World Map**: Select a layer via QuickMapServices and a TIFF image.

3. **🔗 Control Points Selection**
   - Select points on the base layer and the image to establish correspondences.

4. **🎯 Georeferencing**
   - Execute the process and save the georeferenced image.

## 🤝 Contributions

Contributions are welcome! Feel free to submit a pull request or report issues in the repository.

## 📧 Contact

For inquiries or suggestions, please contact the author at facundomedina2320@gmail.com.
