from .model import modelsData


class RandomBundleData(modelsData):
    def __init__(
        self,
        Name: str,
        Index: int,
        Sprite: str,
        Color: str,
        Items: str,
        Pick: int,
        Reward: str,
        RequiredItems: int = -1
    ):
        super().__init__(None)
        self.Name = Name
        self.Index = Index
        self.Sprite = Sprite
        self.Color = Color
        self.Items = Items
        self.Pick = Pick
        self.Reward = Reward
        self.RequiredItems = RequiredItems


class BundleSetsData(modelsData):
    def __init__(
        self,
        Id: str,
        Bundles: list[RandomBundleData]
    ):
        super().__init__(None)
        self.Id = Id
        self.Bundles = Bundles


class RandomBundlesData(modelsData):
    def __init__(
        self,
        AreaName: str,
        Keys: str,
        BundleSets: list[BundleSetsData],
        Bundles: list[RandomBundleData]
    ):
        super().__init__(None)
        self.AreaName = AreaName
        self.Keys = Keys
        self.BundleSets = BundleSets
        self.Bundles = Bundles

