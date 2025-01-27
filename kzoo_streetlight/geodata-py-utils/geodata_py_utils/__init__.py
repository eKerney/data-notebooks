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
    '''GeoData Baseclass
    :return: New instance of GeoData
    :rtype: GeoData
    '''
    def __init__(self, file_path: str = "", input_type: InputTypes = InputTypes.DATA_PATH):
        if not file_path:
            self.gdf = None
            logging.warning('NO PATH SPECIFIED')
        elif input_type == InputTypes.DATA_PATH or input_type == InputTypes.DATA_URL:
            self.gdf = gpd.read_file(file_path)
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
    def gdf(self):
        return self._gdf

    @gdf.setter
    def gdf(self, value):
        self._gdf = value


#  class GeoJSONtools:
#     def __init__(self, file_path: str = "", typ: str = "json"):
#         if not file_path:
#             self.geojson = None
#         elif file_path.startswith("https:") or file_path.startswith("http:"):
#             gdf = gpd.read_file(file_path)
#             self.geojson = json.loads(gdf.to_json())
#         else:
#             f = open(file_path)
#             splt = file_path.split('/')
#             print(f'Loaded JSON: {splt[-1]}')
#             self.geojson = json.load(f)

#     @property
#     def geojson(self):
#         return self._geojson

#     @geojson.setter
#     def geojson(self, value):
#         self._geojson = value

#     def export_file(self, file_name="geojson_file.geojson"):
#         with open((f'{file_name}.geojson'), "w") as outfile:
#             outfile.write(json.dumps(self.geojson))
#         print(f'GeoJSON output: {file_name}.geojson')
