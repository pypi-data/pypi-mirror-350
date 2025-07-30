from encodings.punycode import T
from token import OP
from typing import Optional

class dialogueKeyModel:
    def __init__(self):
        self.key=""
    
    def getJson(self) -> str:
        return self.key
class dialogueKey(dialogueKeyModel):
    def __init__(self, key:Optional[str]=""):
        super().__init__()
        self.key=key

dialogue_keys = {
    "breakUp":True,
    "divorced":True,
    "DumpsterDiveComment":True,
    "GreenRain":True,
    "GreenRain_2":True,
    "HitBySlingshot":True,
    "Resort":True,
    "Resort_Bar":True,
    "Resort_Chair":True,
    "Resort_Dance":True,
    "Resort_Entering":True,
    "Resort_Leaving":True,
    "Resort_Shore":True,
    "Resort_Towel":True,
    "Resort_Umbrella":True,
    "Resort_Wander":True,
    
    "SpouseFarmhouseClutter":True,
    "SpouseGiftJealous":True,
    "Spouse_MonstersInHouse":True,
    "SpouseStardrop":True,
    "WipedMemory":True,
    "AcceptBirthdayGift": False,
    "AcceptBirthdayGift_Negative":True,
    "AcceptBirthdayGift_Positive":True,
    "AcceptBouquet":True,
    "AcceptGift":False,
    "MovieInvitation":True,
    "RejectBouquet": True,
    "RejectBouquet_NotDatable":True,
    "RejectBouquet_NpcAlreadyMarried":True,
    "RejectBouquet_AlreadyAccepted_Engaged":True,
    "RejectBouquet_AlreadyAccepted_Married":True,
    "RejectBouquet_AlreadyAccepted":True,
    "RejectBouquet_Divorced":True,
    "RejectBouquet_VeryLowHearts":True,
    "RejectBouquet_LowHearts":True,
    
    "RejectGift_Divorced":True,
    "RejectItem":False,
    "RejectMermaidPendant":True,
    "RejectMermaidPendant_Engaged":True,
    "RejectMermaidPendant_AlreadyAccepted_Married":True,
    "RejectMermaidPendant_AlreadyAccepted":True,
    "RejectMermaidPendant_Divorced":True,
    "RejectMermaidPendant_NeedHouseUpgrade":True,
    "RejectMermaidPendant_NotDatable":True,
    "RejectMermaidPendant_NpcWithSomeoneElse":True,
    "RejectMermaidPendant_PlayerWithSomeoneElse":True,
    "RejectMermaidPendant_Under8Hearts":True,
    "RejectMermaidPendant_Under10Hearts":True,
    "RejectMermaidPendant_Under10Hearts_AskedAgain":True,
    
    "RejectMovieTicket_AlreadyInvitedBySomeoneElse":True,
    "RejectMovieTicket_AlreadyWatchedThisWeek":True,
    "RejectMovieTicket_Divorced":True,
    "RejectMovieTicket_DontWantToSeeThatMovie":True,
    "RejectMovieTicket":True,

    "RejectRoommateProposal_AlreadyAccepted":True,
    "RejectRoommateProposal_NpcWithSomeoneElse":True,
    "RejectRoommateProposal_PlayerWithSomeoneElse":True,
    "RejectRoommateProposal_LowFriendship":True,
    "RejectRoommateProposal_SmallHouse":True,
    "RejectRoommateProposal":True,
    "accept":False,
    "rekect":False,
    "Fair_Judging":True,
    "Fair_Judged_PlayerLost_PurpleShorts":True,
    "Fair_Judged_PlayerLost_Skipped":True,
    "Fair_Judged_PlayerLost":True,
    "Fair_Judged_PlayerWon":True,
    "Fair_Judged":True,
    "FlowerDance_Accept_Roommate":True,
    "FlowerDance_Accept_Spouse":True,
    "FlowerDance_Accept":True,
    "FlowerDance_Decline":True,
    "WinterStar_GiveGift_Before_Roommate":True,
    "WinterStar_GiveGift_Before_Spouse":True,
    "WinterStar_GiveGift_Before":True,
    "WinterStar_GiveGift_After_Roommate":True,
    "WinterStar_GiveGift_After_Spouse":True,
    "WinterStar_GiveGift_After":True,

    "WinterStar_ReceiveGift":False
}

def create_dialogue_class(key_name: str):
    class _DialogueSubclass(dialogueKeyModel):
        def __init__(self):
            super().__init__()
            self.key = key_name

    _DialogueSubclass.__name__ = key_name
    return _DialogueSubclass

def create_dialogue_class_exp(key_name: str):
    class _DialogueSubclass(dialogueKeyModel):
        def __init__(self, exp: Optional[str] = ""):
            super().__init__()
            self.key = key_name+"_"+exp

    _DialogueSubclass.__name__ = key_name
    return _DialogueSubclass



for key, value in dialogue_keys.items():
    if value:
        setattr(dialogueKey, key, create_dialogue_class(key))
    else:
        setattr(dialogueKey, key, create_dialogue_class_exp(key))







class dialogueValueData:
    def __init__(self):
        pass

class dialogueData:
    def __init__(self, key:dialogueKey, value:dialogueValueData):
        self.key=key
        self.value=value