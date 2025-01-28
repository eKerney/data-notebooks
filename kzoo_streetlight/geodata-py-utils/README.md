# geodata-py-utils

This is a simple python utility built primaryily on top of the wonderful GeoPandas library, a python Geospatial tool that utilizes the power of GDAL.  The utility makes loading, exploring, analyzing and visualizing spatial data even more efficient in a Jupyter Notebook.  

### Loading Data 
`Class GeoData`
input_type is a custom python string enum:
```python
class InputTypes(Enum):
    DATA_PATH = 'FILE_PATH'
    DATA_URL = 'DATA_URL'
    DATA_FILE = 'DATA_FILE'
    DATA_STRING = 'DATA_STRING'
```
DATA_PATH uses the geopandas.read_file() function under the hood, and is well tested with:
- ESRI Shapefile
- FlatGeobuf
- GeoJSON
- GPKG

        
DATA_URL also uses read_file(), and works best with GeoJSON as other formats have not been tested.






