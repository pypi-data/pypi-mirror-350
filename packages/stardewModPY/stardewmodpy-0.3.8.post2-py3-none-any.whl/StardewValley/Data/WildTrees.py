from .model import modelsData
from typing import Any, Optional

class WildTreesData(modelsData):
    def __init__(
            self,
            key: str,
            Textures: list[dict[str, str]],
            SeedItemId: str,
            SeedPlantable: bool,
            GrowthChance: float,
            FertilizedGrowthChance: float,
            SeedSpreadChance: float,
            SeedOnShakeChance: float,
            SeedOnChopChance: float,
            DropWoodOnChop: bool,
            DropHardwoodOnLumberChop: bool,
            IsLeafy: bool,
            IsLeafyInWinter: bool,
            IsLeafyInFall: bool,            
            GrowsInWinter: bool,
            IsStumpDuringWinter: bool,
            AllowWoodpeckers: bool,
            UseAlternateSpriteWhenNotShaken: bool,
            UseAlternateSpriteWhenSeedReady: bool,
            GrowsMoss:bool,
            DebrisColor: Optional[str] = None,
            PlantableLocationRules: Optional[Any] = None,
            SeedDropItems: Optional[list[dict[str, Any]]] = None,
            ChopItems: Optional[list[dict[str, Any]]] = None,
            TapItems: Optional[list[dict[str, Any]]] = None,
            ShakeItems: Optional[Any] = None,
            CustomFields: Optional[str] = None
        ):
        super().__init__(key)

        self.Textures = Textures
        self.SeedItemId = SeedItemId
        self.SeedPlantable = SeedPlantable
        self.GrowthChance = GrowthChance
        self.FertilizedGrowthChance = FertilizedGrowthChance
        self.SeedSpreadChance = SeedSpreadChance
        self.SeedOnShakeChance = SeedOnShakeChance
        self.SeedOnChopChance = SeedOnChopChance
        self.DropWoodOnChop = DropWoodOnChop
        self.DropHardwoodOnLumberChop = DropHardwoodOnLumberChop
        self.IsLeafy = IsLeafy
        self.IsLeafyInWinter = IsLeafyInWinter
        self.IsLeafyInFall = IsLeafyInFall
        self.GrowsInWinter = GrowsInWinter
        self.IsStumpDuringWinter = IsStumpDuringWinter
        self.AllowWoodpeckers = AllowWoodpeckers
        self.UseAlternateSpriteWhenNotShaken = UseAlternateSpriteWhenNotShaken
        self.UseAlternateSpriteWhenSeedReady = UseAlternateSpriteWhenSeedReady
        self.DebrisColor = DebrisColor
        self.PlantableLocationRules = PlantableLocationRules
        self.SeedDropItems = SeedDropItems if SeedDropItems is not None else []
        self.ChopItems = ChopItems if ChopItems is not None else []
        self.TapItems = TapItems if TapItems is not None else []
        self.ShakeItems = ShakeItems
        self.CustomFields = CustomFields
        self.GrowsMoss=GrowsMoss
