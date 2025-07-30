from .model import modelsData
from typing import Optional, Any


class PowersData(modelsData):
    def __init__(
        self,
        key: str,
        DisplayName: str,
        TexturePath: str,
        TexturePosition: dict[str, int],
        UnlockedCondition: str,
        Description: Optional[str] = "",
        CustomFields: Optional[Any] = None
    ):
        super().__init__(key)
        self.DisplayName = DisplayName
        self.TexturePath = TexturePath
        self.TexturePosition = TexturePosition
        self.UnlockedCondition = UnlockedCondition
        self.Description = Description
        self.CustomFields = CustomFields


    
