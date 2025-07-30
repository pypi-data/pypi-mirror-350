from .model import modelsData
from typing import Optional, Any


class GiantCropsData(modelsData):
    def __init__(
        self,
        key: str,
        FromItemId: str,
        HarvestItems: list[dict[str, Any]],
        Texture: str,
        TexturePosition: Optional[dict[str, int]] = {"X": 0, "Y": 0},
        TileSize: Optional[dict[str, int]] = {"X": 3, "Y": 3},
        Health: Optional[int] = 3,
        Chance: Optional[float] = 0.01,
        Condition: Optional[str] = None,
        CustomFields: Optional[Any] = None
    ):
        super().__init__(key)
        self.FromItemId = FromItemId
        self.HarvestItems = HarvestItems
        self.Texture = Texture
        self.TexturePosition = TexturePosition
        self.TileSize = TileSize
        self.Health = Health
        self.Chance = Chance
        self.Condition = Condition
        self.CustomFields = CustomFields
