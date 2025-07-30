from .model import modelsData
from typing import Optional, Any


class ObjectivesData(modelsData):
    def __init__(
        self,
        Type: str,
        Text: str,
        RequiredCount: str,
        Data: dict[str, str]
    ):
        super().__init__(None)
        self.Type = Type
        self.Text = Text
        self.RequiredCount = RequiredCount
        self.Data = Data



class RewardsData(modelsData):
    def __init__(
        self,
        Type: str,
        Data: dict[str, Any]
    ):
        super().__init__(None)
        self.Type = Type
        self.Data = Data



class RandomizeElementsData(modelsData):
    def __init__(
        self,
        Name: str,
        Values: list[dict[str, str]]
    ):
        super().__init__(None)
        self.Name = Name
        self.Values = Values



class SpecialOrdersData(modelsData):
    def __init__(
        self,
        key: str,
        Requester: str,
        Duration: str,
        Repeatable: bool,
        RequiredTags: str,
        OrderType: str,
        SpecialRule: str,
        Text: str,
        Objectives: list[ObjectivesData],
        Rewards: list[RewardsData],
        ItemToRemoveOnEnd: str = None,
        MailToRemoveOnEnd: str = None,
        RandomizedElements: list[RandomizeElementsData] = None,
        CustomFields: Optional[Any] = None
    ):
        super().__init__(key)
        self.Requester = Requester
        self.Duration = Duration
        self.Repeatable = Repeatable
        self.RequiredTags = RequiredTags
        self.OrderType = OrderType
        self.SpecialRule = SpecialRule
        self.Text = Text
        self.Objectives = Objectives
        self.Rewards = Rewards
        self.ItemToRemoveOnEnd = ItemToRemoveOnEnd
        self.MailToRemoveOnEnd = MailToRemoveOnEnd
        self.RandomizedElements = RandomizedElements
        self.CustomFields = CustomFields
