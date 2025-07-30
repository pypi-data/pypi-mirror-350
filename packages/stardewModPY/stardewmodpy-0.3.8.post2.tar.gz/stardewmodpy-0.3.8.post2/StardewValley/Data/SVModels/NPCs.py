from ...helper import Helper
from ...contentpatcher import EditData, Load
from .svmodel import svmodel
from ..Characters import CharactersData


class NPCs(svmodel):
    """
    The recommended file is one for each item in the npcsList list, with the class inheriting from CharactersData
    Example: class NameNpc(CharactersData):
    npcsList=[NameNpc(), OtherNpc()]
    For the complete loading of NPCs, it is important that for each NPC added to self.npcsList there is also a file in assets/NPCs/Characters/NameNPC.png and within assets/NPCs/Portraits/NameNPC.png << replacing NameNPC with the name of the class added to the npcsList
    """
    def __init__(self, mod: Helper, npcsList:list[CharactersData]):
        self.npcsList=npcsList
        super().__init__(mod)
        
    
    def contents(self):
        super().contents()
        
        for npc in self.npcsList:
            self.registryContentData(
                Load(
                    LogName=f"Carregando sprite {npc.key}",
                    Target=f"Characters/{npc.key}",
                    FromFile=f"assets/NPCs/Characters/{npc.key}.png"
                )
            )
            self.registryContentData(
                Load(
                    LogName=f"Carregando portrait {npc.key}",
                    Target=f"Portraits/{npc.key}",
                    FromFile=f"assets/NPCs/Portraits/{npc.key}.png"
                )
            )
            self.registryContentData(
                EditData(
                    LogName=f"Add {npc.key}",
                    Target="Data/Characters",
                    Entries={
                        npc.key:npc.getJson()
                    }
                )
            )