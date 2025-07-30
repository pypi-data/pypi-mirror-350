from .model import modelsData
from typing import Optional


class FencesData(modelsData):
    def __init__(
        self, 
        key: str,
        Health: int,
        Texture: str,
        PlacementSound: str,
        RemovalToolIds: list[str] = [],
        RemovalToolTypes: list[str] = [],
        RemovalSound: Optional[str] = "axchop",
        RemovalDebrisType: Optional[int] = 14,
        RepairHealthAdjustmentMinimum: Optional[float] = 0.0,
        RepairHealthAdjustmentMaximum: Optional[float] = 0.0,
        HeldObjectDrawOffset: Optional[str] = "0, -20",
        LeftEndHeldObjectDrawX: Optional[float] = 0.0,
        RightEndHeldObjectDrawX: Optional[float] = 0.0
    ):
        super().__init__(key)
        self.Health = Health
        self.Texture = Texture
        self.PlacementSound = PlacementSound
        self.RemovalToolIds = RemovalToolIds
        self.RemovalToolTypes = RemovalToolTypes
        self.RemovalSound = RemovalSound
        self.RemovalDebrisType = RemovalDebrisType
        self.RepairHealthAdjustmentMinimum = RepairHealthAdjustmentMinimum
        self.RepairHealthAdjustmentMaximum = RepairHealthAdjustmentMaximum
        self.HeldObjectDrawOffset = HeldObjectDrawOffset
        self.LeftEndHeldObjectDrawX = LeftEndHeldObjectDrawX
        self.RightEndHeldObjectDrawX = RightEndHeldObjectDrawX
