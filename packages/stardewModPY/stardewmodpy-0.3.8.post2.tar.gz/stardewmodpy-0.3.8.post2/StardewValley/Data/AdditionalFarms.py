from typing import Optional, Dict, Any
from .model import modelsData
import json

class AdditionalFarmsData(modelsData):
    def __init__(
        self,
        key: int,
        Id: str,
        TooltipStringPath: str,
        MapName: str,
        IconTexture: str,
        WorldMapTexture: str,
        SpawnMonstersByDefault: bool = False,
        ModData: Optional[Dict[str, Any]] = None,
        CustomFields:  Optional[dict[str,str]] = None
    ):        
        super().__init__(key)
        self.Id = Id
        self.TooltipStringPath = TooltipStringPath
        self.MapName = MapName
        self.IconTexture = IconTexture
        self.WorldMapTexture = WorldMapTexture
        self.SpawnMonstersByDefault = SpawnMonstersByDefault
        self.ModData = ModData if ModData is not None else {}
        self.CustomFields = CustomFields
