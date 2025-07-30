from typing import Optional, List
from .model import modelsData

class CustomAttributes(modelsData):
    def __init__(
        self,
        CombatLevel:float,
        FarmingLevel:float,
        FishingLevel:float,
        ForagingLevel:float,
        LuckLevel:float,
        MiningLevel:float,
        Attack:float,
        AttackMultiplier:float,
        CriticalChanceMultiplier:float,
        CriticalPowerMultiplier:float,
        Defense:float,
        Immunity:float,
        KnockbackMultiplier:float,
        MagneticRadius:float,
        MaxStamina:float,
        Speed:float,
        WeaponPrecisionMultiplier:float,
        WeaponSpeedMultiplier:float
    ):
        self.CombatLevel=CombatLevel
        self.FarmingLevel=FarmingLevel
        self.FishingLevel=FishingLevel
        self.ForagingLevel=ForagingLevel
        self.LuckLevel=LuckLevel
        self.MiningLevel=MiningLevel
        self.Attack=Attack
        self.AttackMultiplier=AttackMultiplier
        self.CriticalChanceMultiplier=CriticalChanceMultiplier
        self.CriticalPowerMultiplier=CriticalPowerMultiplier
        self.Defense=Defense
        self.Immunity=Immunity
        self.KnockbackMultiplier=KnockbackMultiplier
        self.MagneticRadius=MagneticRadius
        self.MaxStamina=MaxStamina
        self.Speed=Speed
        self.WeaponPrecisionMultiplier=WeaponPrecisionMultiplier
        self.WeaponSpeedMultiplier=WeaponSpeedMultiplier
        
class ObjectsBuffsData(modelsData):
    def __init__(
        self,
        *,
        Id:str,
        Duration: Optional[int]=0,
        BuffId: Optional[str]=None,
        IsDebuff: Optional[bool]=None,
        IconTexture: Optional[str]=None,
        IconSpriteIndex: Optional[int]=None,
        GlowColor: Optional[str]=None,
        CustomAttributes: Optional[CustomAttributes]=None,
        CustomFields: Optional[dict[str, str]]=None
    ):
        super().__init__(None)
        self.Id=Id
        self.BuffId=BuffId
        self.IconTexture=IconTexture
        self.IconSpriteIndex=IconSpriteIndex
        self.Duration=Duration
        self.IsDebuff=IsDebuff
        self.GlowColor=GlowColor
        self.CustomAttributes=CustomAttributes
        self.CustomFields=CustomFields


class ObjectsData(modelsData):
    def __init__(
            self,
            key: str,
            Name: str,
            DisplayName: str,
            Description: str,
            Type: str,
            Category: int,
            Price: Optional[int]=None, 
            Texture: Optional[str] = None,
            SpriteIndex: Optional[int] = None,
            ColorOverlayFromNextIndex: Optional[bool] = None, 
            Edibility: Optional[int] = None,
            IsDrink: Optional[bool] = None,
            Buffs: Optional[List[ObjectsBuffsData]] = None, 
            GeodeDropsDefaultItems: bool = None,
            GeodeDrops: Optional[List[str]] = None, 
            ArtifactSpotChances: Optional[str] = None,
            CanBeGivenAsGift: bool = None, 
            CanBeTrashed: bool = None,
            ExcludeFromFishingCollection: bool = None, 
            ExcludeFromShippingCollection: bool = None,
            ExcludeFromRandomSale: bool = None, 
            ContextTags: Optional[List[str]] = None,
            CustomFields: Optional[dict[str, str]] = None
        ):
        
        super().__init__(key)
        # Atribuindo valores padrão para listas e outros mutáveis
        self.Name = Name
        self.DisplayName = DisplayName
        self.Description = Description
        self.Type = Type
        self.Category = Category
        self.Price = Price
        self.Texture = Texture
        self.SpriteIndex = SpriteIndex
        self.ColorOverlayFromNextIndex = ColorOverlayFromNextIndex
        self.Edibility = Edibility
        self.IsDrink = IsDrink
        self.Buffs = Buffs
        self.GeodeDropsDefaultItems = GeodeDropsDefaultItems
        self.GeodeDrops = GeodeDrops
        self.ArtifactSpotChances = ArtifactSpotChances
        self.CanBeGivenAsGift = CanBeGivenAsGift
        self.CanBeTrashed = CanBeTrashed
        self.ExcludeFromFishingCollection = ExcludeFromFishingCollection
        self.ExcludeFromShippingCollection = ExcludeFromShippingCollection
        self.ExcludeFromRandomSale = ExcludeFromRandomSale
        self.ContextTags = ContextTags
        self.CustomFields = CustomFields