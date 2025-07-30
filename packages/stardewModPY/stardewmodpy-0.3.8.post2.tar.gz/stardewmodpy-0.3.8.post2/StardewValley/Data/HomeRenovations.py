from .model import modelsData
from typing import Optional, Any


class HomeRenovationsData(modelsData):
    def __init__(
        self, 
        key: str,
        TextStrings: str,
        Requirements: list[dict[str, str]],
        RenovateActions: list[dict[str, str]],
        RectGroups: list[dict[str, list[dict[str, int]]]],
        AnimationType: Optional[str] = "build",
        CheckForObstructions: Optional[bool] = False,
        SpecialRect: Optional[str] = None,
        CustomFields: Optional[Any] = None
    ):
        super().__init__(key)
        self.TextStrings = TextStrings
        self.Requirements = Requirements
        self.RenovateActions = RenovateActions
        self.RectGroups = RectGroups
        self.AnimationType = AnimationType
        self.CheckForObstructions = CheckForObstructions
        self.SpecialRect = SpecialRect
        self.CustomFields = CustomFields


    
