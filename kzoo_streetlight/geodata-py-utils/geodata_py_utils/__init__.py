import geopandas as gpd
import json
import logging
from enum import Enum


class InputTypes(Enum):
    DATA_PATH = 'FILE_PATH'
    DATA_URL = 'DATA_URL'
    DATA_FILE = 'DATA_FILE'
    DATA_STRING = 'DATA_STRING'


class GeoData:
    """
    GeoData Baseclass built on the back of GeoPandas & GDAL

    Parameters
    ----------
    file_path : str = ""
        Path to the local file, URL to GeoJSON, or in memoery GeoJSON string.
    input_type : InputTypes = InputTypes.DATA_PATH
        Path InputType string Enum:
        `InputTypes.DATA_PATH`: GeoPandas ``read_file`` method reading
            data from a local file
        `InputTypes.DATA_URL`: GeoPandas ``read_file`` method reading GeoJSON
            from a URL
        `InputTypes.DATA_FILE`: Use builtin python ``open`` to read file, then
            `json.load` into GeoPandas ``read_file``
        `InputTypes.DATA_STRING`: Load in memory data directly as a string,
            then `json.load` into GeoPandas ``read_file``
    row_filter : int = 0
        from Load first `x` rows into GeoDataframe

    Examples
    --------
    >>> url_path = 'https://raw.githubusercontent.com/martynafford/natural-earth-geojson/refs/heads/master/110m/cultural/ne_110m_admin_0_countries.json'
    >>> geo_data = GeoData(url_path, InputTypes.DATA_URL, row_filter=10)
    >>> geo_data.gdf
    scalerank       featurecla  LABELRANK   SOVEREIGNT SOV_A3  ADM0_DIF  LEVEL  \
    0          1  Admin-0 country        3.0  Afghanistan    AFG       0.0    2.0   
    1          1  Admin-0 country        3.0       Angola    AGO       0.0    2.0   
    ...
                                                geometry  
    0  POLYGON ((61.21082 35.65007, 62.23065 35.27066...  
    1  MULTIPOLYGON (((23.90415 -11.72228, 24.07991 -...  
    [2 rows x 72 columns]
    """

    def __init__(
            self,
            file_path: str = "",
            input_type: InputTypes = InputTypes.DATA_PATH,
            row_filter: int = 0
            ):
        """
        Generates new GeoData object, see parameters above.
        Loads data into GeoPandas dataframe as `self.gdf` attribute
        """

        if not file_path:
            self.gdf = None
            logging.warning('NO PATH SPECIFIED')
        elif input_type == InputTypes.DATA_PATH or input_type == InputTypes.DATA_URL:
            self.gdf = gpd.read_file(file_path) if not row_filter else gpd.read_file(file_path, rows=row_filter)
            logging.info(f'Loaded Data: {file_path}')
        elif input_type == InputTypes.DATA_FILE:
            f = open(file_path)
            splt = file_path.split('/')
            logging.info(f'Loaded File: {splt[-1]}')
            self.gdf = gpd.read_file(json.load(f))
        elif input_type == InputTypes.DATA_STRING:
            logging.info(f'Loaded Data: {file_path}')
            self.gdf = gpd.read_file(json.load(file_path))

    @property
    def gdf(self) -> gpd.GeoDataFrame:
        return self._gdf

    @gdf.setter
    def gdf(self, value):
        self._gdf = value

    @property
    def geojson(self) -> json:
        return json.loads(self.gdf.to_json())

    @geojson.setter
    def geojson(self, value):
        self._geojson = value

    def export_geojson(self, file_name="geojson_file.geojson") -> None:
        with open((f'{file_name}.geojson'), "w") as outfile:
            outfile.write(json.dumps(self.geojson))
        print(f'GeoJSON output: {file_name}.geojson')
