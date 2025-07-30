from .model import modelsData
from typing import Any, Optional

class ToolsData(modelsData):
    def __init__(
            self,
            key: str,
            ClassName: str,
            Name: str,
            DisplayName: str,
            Description: str,
            Texture: str,
            SpriteIndex: int,
            MenuSpriteIndex: int,
            UpgradeLevel: int,
            SalePrice: Optional[int]=-1,
            AttachmentSlots: Optional[int]=-1,
            ConventionalUpgradeFrom: Optional[str] = None,
            UpgradeFrom: Optional[list[dict[str, Any]]] = None,
            CanBeLostOnDeath: bool = False,
            SetProperties: Optional[Any] = None,
            ModData: Optional[Any] = None,
            CustomFields: Optional[Any] = None
        ):
        super().__init__(key)

        self.ClassName = ClassName
        self.Name = Name
        self.AttachmentSlots = AttachmentSlots
        self.SalePrice = SalePrice
        self.DisplayName = DisplayName
        self.Description = Description
        self.Texture = Texture
        self.SpriteIndex = SpriteIndex
        self.MenuSpriteIndex = MenuSpriteIndex
        self.UpgradeLevel = UpgradeLevel
        self.ConventionalUpgradeFrom = ConventionalUpgradeFrom
        self.UpgradeFrom = UpgradeFrom
        self.CanBeLostOnDeath = CanBeLostOnDeath
        self.SetProperties = SetProperties
        self.ModData = ModData
        self.CustomFields = CustomFields

    
