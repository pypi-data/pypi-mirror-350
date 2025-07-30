from .model import modelsData
from typing import Optional, Any


class CranePrizesData(modelsData):
    def __init__(
        self,
        Id: str,
        ItemId: str,
        Rarity: Optional[int] = 1,
        RandomItemId: Optional[list[str]] = None,
        Condition: Optional[str] = None,
        PerItemCondition: Optional[str] = None,
        MaxItems: Optional[Any] = None,
        IsRecipe: Optional[bool] = False,
        Quality: Optional[int] = -1,
        MinStack: Optional[int] = -1,
        MaxStack: Optional[int] = -1,
        ObjectInternalName: Optional[str] = None,
        ObjectDisplayName: Optional[str] = None,
        ObjectColor: Optional[Any] = None,
        ToolUpgradeLevel: Optional[int] = -1,
        QualityModifiers: Optional[Any] = None,
        StackModifiers: Optional[Any] = None,
        QualityModifierMode: Optional[str] = "Stack",
        StackModifierMode: Optional[str] = "Stack",
        ModData: Optional[dict[str, str]] = None
    ):
        super().__init__(None)
        self.Id = Id
        self.ItemId = ItemId
        self.Rarity = Rarity
        self.RandomItemId = RandomItemId
        self.Condition = Condition
        self.PerItemCondition = PerItemCondition
        self.MaxItems = MaxItems
        self.IsRecipe = IsRecipe
        self.Quality = Quality
        self.MinStack = MinStack
        self.MaxStack = MaxStack
        self.ObjectInternalName = ObjectInternalName
        self.ObjectDisplayName = ObjectDisplayName
        self.ObjectColor = ObjectColor
        self.ToolUpgradeLevel = ToolUpgradeLevel
        self.QualityModifiers = QualityModifiers
        self.StackModifiers = StackModifiers
        self.QualityModifierMode = QualityModifierMode
        self.StackModifierMode = StackModifierMode
        self.ModData = ModData



class ScenesData(modelsData):
    def __init__(
        self,
        Image: int,
        Music: str,
        Sound: str,
        MessageDelay: int,
        Script: str,
        Text: str,
        Shake: bool,
        ResponsePoint: str | None,
        ID: str
    ):
        super().__init__(None)
        self.Image = Image
        self.Music = Music
        self.Sound = Sound
        self.MessageDelay = MessageDelay
        self.Script = Script
        self.Text = Text
        self.Shake = Shake
        self.ResponsePoint = ResponsePoint
        self.ID = ID



class MoviesData(modelsData):
    def __init__(
        self,
        Id: str,
        SheetIndex: int,
        Title: str,
        Description: str,
        Tags: list[str],
        CranePrizes: list[CranePrizesData],
        Scenes: list[ScenesData],
        ClearDefaultCranePrizeGroups: list[int] = [],
        CustomFields: Optional[Any] = None
    ):
        super().__init__(None)
        self.Id = Id
        self.SheetIndex = SheetIndex
        self.Title = Title
        self.Description = Description
        self.Tags = Tags
        self.CranePrizes = CranePrizes
        self.Scenes = Scenes
        self.ClearDefaultCranePrizeGroups = ClearDefaultCranePrizeGroups
        self.CustomFields = CustomFields
