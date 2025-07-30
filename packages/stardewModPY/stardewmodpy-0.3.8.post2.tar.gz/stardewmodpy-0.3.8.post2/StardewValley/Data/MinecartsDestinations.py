from .model import modelsData
from typing import Optional, Any


class MinecartsDestinationsData(modelsData):
    def __init__(
            self,
            Id: str,
            DisplayName: str,
            TargetLocation: str,
            TargetTile: dict[str, int],
            TargetDirection: Optional[str] = None,
            Price: Optional[int] = None,
            BuyTicketMessage: Optional[str] = None,
            Condition: Optional[str] = None

        ):
        super().__init__(None)
        self.Id = Id
        self.DisplayName = DisplayName
        self.TargetLocation = TargetLocation
        self.TargetTile = TargetTile
        self.TargetDirection = TargetDirection
        self.Price = Price
        self.BuyTicketMessage = BuyTicketMessage
        self.Condition = Condition
