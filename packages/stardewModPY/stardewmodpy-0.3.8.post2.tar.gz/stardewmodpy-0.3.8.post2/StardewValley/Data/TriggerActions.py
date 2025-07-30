from .model import modelsData
from typing import Any, Optional, List

class Actions:
    def __init__(self):
        pass

    def AddBuff(self, buffID: str, duration: int = None):
        return f"AddBuff {buffID}" + (f" {duration}" if duration is not None else "")

    def RemoveBuff(self, buffID: str):
        return f"RemoveBuff {buffID}"

    def AddConversationTopic(self, topic: str, dayDuration: int = 0):
        return f"AddConversationTopic {topic} {dayDuration}"

    def RemoveConversationTopic(self, topic: str):
        return f"RemoveConversationTopic {topic}"

    def AddFriendshipPoints(self, npc: str, count: int):
        return f"AddFriendshipPoints {npc} {count}"

    def AddItem(self, itemID: str, count: int = 1, quality: int = 0):
        return f"AddItem {itemID} {count} {quality}"

    def RemoveItem(self, itemID: str, count: int = 1):
        return f"RemoveItem {itemID} {count}"

    def AddMail(self, player: str, mailID: str, mailType: str = "tomorrow"):
        return f"AddMail {player} {mailID} {mailType}"

    def RemoveMail(self, player: str, mailID: str, mailType: str = "all"):
        return f"RemoveMail {player} {mailID} {mailType}"

    def AddMoney(self, amount: int):
        return f"AddMoney {amount}"

    def AddQuest(self, questID: str):
        return f"AddQuest {questID}"

    def RemoveQuest(self, questID: str):
        return f"RemoveQuest {questID}"

    def AddSpecialOrder(self, orderID: str):
        return f"AddSpecialOrder {orderID}"

    def RemoveSpecialOrder(self, orderID: str):
        return f"RemoveSpecialOrder {orderID}"

    def If(self, query: str, action_true: str, action_false: str = None):
        if action_false:
            return f"If {query} ## {action_true} ## {action_false}"
        return f"If {query} ## {action_true}"

    def IncrementStat(self, statKey: str, amount: int = 1):
        return f"IncrementStat {statKey} {amount}"

    def MarkActionApplied(self, player: str, answerID: str, applied: bool = True):
        return f"MarkActionApplied {player} {answerID} {str(applied).lower()}"

    def MarkCookingRecipeKnown(self, player: str, recipeID: str, known: bool = True):
        return f"MarkCookingRecipeKnown {player} {recipeID} {str(known).lower()}"

    def MarkCraftingRecipeKnown(self, player: str, recipeKey: str, known: bool = True):
        return f"MarkCraftingRecipeKnown {player} {recipeKey} {str(known).lower()}"

    def MarkEventSeen(self, player: str, eventID: str, seen: bool = True):
        return f"MarkEventSeen {player} {eventID} {str(seen).lower()}"

    def MarkQuestionAnswered(self, player: str, answerID: str, answered: bool = True):
        return f"MarkQuestionAnswered {player} {answerID} {str(answered).lower()}"

    def MarkSongHeard(self, player: str, songID: str, heard: bool = True):
        return f"MarkSongHeard {player} {songID} {str(heard).lower()}"

    def Null(self):
        return "Null"

    def RemoveTemporaryAnimatedSprites(self):
        return "RemoveTemporaryAnimatedSprites"

    def SetNpcInvisible(self, npc: str, days: int):
        return f"SetNpcInvisible {npc} {days}"

    def SetNpcVisible(self, npc: str):
        return f"SetNpcVisible {npc}"

    
    

class TriggerActionsData(modelsData):
    def __init__(
            self,
            key: str,
            Id: str,
            Trigger: str,
            Condition: str=None,
            SkipPermanentlyCondition: Optional[Any] = None,
            HostOnly: bool = False,
            Action: str = None,
            Actions: Optional[List[str]] = None,
            CustomFields: Optional[Any] = None,
            MarkActionApplied: bool = True
        ):
        super().__init__(key)

        self.Id = Id
        self.Trigger = Trigger
        self.Condition = Condition
        self.SkipPermanentlyCondition = SkipPermanentlyCondition
        self.HostOnly = HostOnly
        self.Action = Action
        self.Actions = Actions if Actions is not None else []
        self.CustomFields = CustomFields
        self.MarkActionApplied = MarkActionApplied
