from .svmodel import svmodel
from ...contentpatcher import Load

class MapsModel:
    def __init__(self, *, map_name:str, map_file:str, maps: svmodel):
        self.maps = maps
        self.map_name = map_name
        self.map_file = map_file
        self.contents()
    
    def contents(self):
        self.maps.registryContentData(
            Load(
                LogName=f"Carregando {self.map_name}",
                Target=f"Maps/{self.map_name}",
                FromFile=self.map_file
            )
        )

        