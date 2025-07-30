from .model import modelsData
from typing import Optional, Any


class PetGiftData(modelsData):
    def __init__(
        self,
        Id: str,
        ItemId: str,
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
        ToolUpgradeLevel: Optional[int] = -1,
        QualityModifiers: Optional[Any] = None,
        StackModifiers: Optional[Any] = None,
        QualityModifierMode: Optional[str] = "Stack",
        StackModifierMode: Optional[str] = "Stack",
        MinimumFriendshipThreshold: Optional[int] = 1000,
        Weight: Optional[float] = 1.0,
        ModData: Optional[dict[str, str]] = None
    ):
        super().__init__(None)
        self.Id = Id
        self.ItemId = ItemId
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
        self.ToolUpgradeLevel = ToolUpgradeLevel
        self.QualityModifiers = QualityModifiers
        self.StackModifiers = StackModifiers
        self.QualityModifierMode = QualityModifierMode
        self.StackModifierMode = StackModifierMode
        self.MinimumFriendshipThreshold = MinimumFriendshipThreshold
        self.Weight = Weight
        self.ModData = ModData


class BreedsData(modelsData):
    def __init__(
        self,
        Id: str,
        Texture: str,
        IconTexture: str,
        IconSourceRect: dict[str, int],
        CanBeChosenAtStart: Optional[bool] = True,
        CanBeAdoptedFromMarnie: Optional[bool] = True,
        AdoptionPrice: Optional[int] = 40000,
        BarkOverride: Optional[Any] = None,
        VoicePitch: Optional[float] = 1.0
    ):
        super().__init__(None)
        self.Id = Id
        self.Texture = Texture
        self.IconTexture = IconTexture
        self.IconSourceRect = IconSourceRect
        self.CanBeChosenAtStart = CanBeChosenAtStart
        self.CanBeAdoptedFromMarnie = CanBeAdoptedFromMarnie
        self.AdoptionPrice = AdoptionPrice
        self.BarkOverride = BarkOverride
        self.VoicePitch = VoicePitch


class PetsData(modelsData):
    def __init__(
        self,
        key: str,
        DisplayName: str,
        BarkSound: str,
        ContentSound: str,
        Breeds: list[BreedsData],
        RepeatContentSoundAfter: Optional[int] = -1,
        EmoteOffset: Optional[dict[str, int]] = {"X": 0, "Y": 0},
        EventOffset: Optional[dict[str, int]] = {"X": 0, "Y": 0},
        AdoptionEventLocation: Optional[str] = "Farm",
        AdoptionEventId: Optional[str] = None,
        SummitPerfectionEvent: Optional[dict[str, Any]] = None,
        GiftChance: Optional[float] = 0.2,
        Gifts: Optional[list[PetGiftData]] = None,
        CustomFields: Optional[Any] = None

    ):
        super().__init__(key)
        self.DisplayName = DisplayName
        self.BarkSound = BarkSound
        self.ContentSound = ContentSound
        self.Breeds = Breeds
        self.RepeatContentSoundAfter = RepeatContentSoundAfter
        self.EmoteOffset = EmoteOffset
        self.EventOffset = EventOffset
        self.AdoptionEventLocation = AdoptionEventLocation
        self.AdoptionEventId = AdoptionEventId
        self.SummitPerfectionEvent = SummitPerfectionEvent
        self.GiftChance = GiftChance
        self.Gifts = Gifts
        self.CustomFields = CustomFields
