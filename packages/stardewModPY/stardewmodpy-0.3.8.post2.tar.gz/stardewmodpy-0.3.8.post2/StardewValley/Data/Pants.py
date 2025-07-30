from .model import modelsData
from typing import Optional, Any


class PantsData(modelsData):
    def __init__(
        self,
        key: str,
        Name: Optional[str] = "Pants",
        DisplayName: Optional[str] = "Pants",
        Description: Optional[str] = "A wearable pair of pants",
        Price: Optional[int] = 50,
        Texture: Optional[str] = None,
        SpriteIndex: Optional[int] = 0,
        DefaultColor: Optional[str] = "255 235 203",
        CanBeDyed: Optional[bool] = False,
        IsPrismatic: Optional[bool] = False,
        CanChooseDuringCharacterCustomization: Optional[bool] = False,
        CustomFields: Optional[Any] = None
    ):
        super().__init__(key)
        self.Name = Name
        self.DisplayName = DisplayName
        self.Description = Description
        self.Price = Price
        self.Texture = Texture
        self.SpriteIndex = SpriteIndex
        self.DefaultColor = DefaultColor
        self.CanBeDyed = CanBeDyed
        self.IsPrismatic = IsPrismatic
        self.CanChooseDuringCharacterCustomization = CanChooseDuringCharacterCustomization
        self.CustomFields = CustomFields
