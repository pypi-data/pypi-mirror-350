from .model import modelsData

class Season(modelsData):
    def __init__(self):
        pass
    
    def getJson(self) -> str:
        return "Spring"

    class Spring(modelsData):
        def __init__(self):
            pass
            
        def getJson() -> str:
            return "Spring"
    
    class Summer(modelsData):
        def __init__(self):
            pass

        def getJson() -> str:
            return "Summer"
    
    class Fall(modelsData):
        def __init__(self):
            pass
    
        def getJson() -> str:
            return "Fall"
    
    class Winter(modelsData):
        def __init__(self):
            pass

        def getJson() -> str:
            return "Winter"


class AquariumType(modelsData):
    def __init__(self):
        pass

    def getJson(self) -> str:
        return "eel"
    
    class Eel(modelsData):
        def __init__(self):
            pass

        def getJson(self) -> str:
            return "eel"
    
    class Cephalopod(modelsData):
        def __init__(self):
            pass

        def getJson(self) -> str:
            return "cephalopod"
    
    class Crawl(modelsData):
        def __init__(self):
            pass

        def getJson(self) -> str:
            return "crawl"
    
    class Ground(modelsData):
        def __init__(self):
            pass

        def getJson(self) -> str:
            return "ground"
    
    class Fish(modelsData):
        def __init__(self):
            pass

        def getJson(self) -> str:
            return "fish"
    
    class Front_crawl(modelsData):
        def __init__(self):
            pass

        def getJson(self) -> str:
            return "front_crawl"
        
class AudioCategory(modelsData):
    def __init__(self):
        pass

    def getJson(self) -> str:
        return "Default"
    
    class Default(modelsData):
        def __init__(self):
            pass
        def getJson(self) -> str:
            return "Default"
    
    class Music(modelsData):
        def __init__(self):
            pass
        def getJson(self) -> str:
            return "Music"
    
    class Sound(modelsData):
        def __init__(self):
            pass
        def getJson(self) -> str:
            return "Sound"
    
    class Ambient(modelsData):
        def __init__(self):
            pass
        def getJson(self) -> str:
            return "Ambient"
    
    class Footsteps(modelsData):
        def __init__(self):
            pass
        def getJson(self) -> str:
            return "Footsteps"

class BCFragility(modelsData):
    def __init__(self, fragility:int):
        if fragility < 0 or fragility > 2:
            raise ValueError("The possible values are 0 (pick up with any tool), 1 (destroyed if hit with an axe/hoe/pickaxe, or picked up with any other tool), or 2 (can't be removed once placed). Default 0.")
        self.fragility = fragility

    def getJson(self) -> int:
        return self.fragility
    

class StackSizeVisibility(modelsData):
    def __init__(self):
        pass

    def getJson(self) -> str:
        return "Show"

    class Hide(modelsData):
        def __init__(self):
            pass

        def getJson(self) -> str:
            return "Hide"
    
    class Show(modelsData):
        def __init__(self):
            pass

        def getJson(self) -> str:
            return "Show"
    
    class ShowIfMultiple(modelsData):
        def __init__(self):
            pass

        def getJson(self) -> str:
            return "ShowIfMultiple"

class Quality(modelsData):
    def __init__(self):
        pass

    def getJson(self) -> int:
        return 0
    
    class Normal(modelsData):
        def __init__(self):
            pass

        def getJson(self) -> int:
            return 0
    
    class Silver(modelsData):
        def __init__(self):
            pass

        def getJson(self) -> int:
            return 1
    
    class Gold(modelsData):
        def __init__(self):
            pass

        def getJson(self) -> int:
            return 2
    
    class Iridium(modelsData):
        def __init__(self):
            pass

        def getJson(self) -> int:
            return 3

class QualityModifierMode(modelsData):
    def __init__(self):
        pass

    def getJson(self) -> str:
        return "Stack"

    class Stack(modelsData):
        def __init__(self):
            pass

        def getJson(self) -> str:
            return "Stack"
    
    class Minimum(modelsData):
        def __init__(self):
            pass

        def getJson(self) -> str:
            return "Minimum"
    
    class Maximum(modelsData):
        def __init__(self):
            pass

        def getJson(self) -> str:
            return "Maximum"

class ToolUpgradeLevel(modelsData):
    def __init__(self):
        pass

    def getJson(self) -> int:
        return 0

    class Normal(modelsData):
        def __init__(self):
            pass

        def getJson(self) -> int:
            return 0
    
    class Copper(modelsData):
        def __init__(self):
            pass

        def getJson(self) -> int:
            return 1
    
    class Steel(modelsData):
        def __init__(self):
            pass

        def getJson(self) -> int:
            return 2
    
    class Gold(modelsData):
        def __init__(self):
            pass

        def getJson(self) -> int:
            return 3
    
    class IridiumTool(modelsData):
        def __init__(self):
            pass

        def getJson(self) -> int:
            return 4
    
    class Bamboo(modelsData):
        def __init__(self):
            pass

        def getJson(self) -> int:
            return 0
    
    class Training(modelsData):
        def __init__(self):
            pass

        def getJson(self) -> int:
            return 1
    
    class Fiberglass(modelsData):
        def __init__(self):
            pass

        def getJson(self) -> int:
            return 2
    
    class IridiumRod(modelsData):
        def __init__(self):
            pass

        def getJson(self) -> int:
            return 3
    
    class AdvancedIridiumRod(modelsData):
        def __init__(self):
            pass

        def getJson(self) -> int:
            return 4

class Modification(modelsData):
    def __init__(self):
        pass

    def getJson(self) -> str:
        return "Multiply"
    
    class Multiply(modelsData):
        def __init__(self):
            pass
        
        def getJson(self) -> str:
            return "Multiply"
    
    class Add(modelsData):
        def __init__(self):
            pass
        
        def getJson(self) -> str:
            return "Add"
    
    class Subtract(modelsData):
        def __init__(self):
            pass
        
        def getJson(self) -> str:
            return "Subtract"
    
    class Divide(modelsData):
        def __init__(self):
            pass
        
        def getJson(self) -> str:
            return "Divide"
    
    class Set(modelsData):
        def __init__(self):
            pass
        
        def getJson(self) -> str:
            return "Set"

class AvailableStockLimit(modelsData):
    def __init__(self):
        pass

    def getJson(self) -> str:
        return "None"
    
    class none(modelsData):
        def __init__(self):
            pass
        
        def getJson(self) -> str:
            return "None"
    
    class Player(modelsData):
        def __init__(self):
            pass
        
        def getJson(self) -> str:
            return "Player"
    
    class Global(modelsData):
        def __init__(self):
            pass
        
        def getJson(self) -> str:
            return "Global"

class Gender(modelsData):
    def __init__(self):
        pass

    def getJson(self) -> str:
        return "Undefined"
    
    class Male(modelsData):
        def __init__(self):
            pass
        
        def getJson(self) -> str:
            return "Male"
    
    class Female(modelsData):
        def __init__(self):
            pass
        
        def getJson(self) -> str:
            return "Female"
    
    class Undefined(modelsData):
        def __init__(self):
            pass
        
        def getJson(self) -> str:
            return "Undefined"
        
class Social(modelsData):
    def __init__(self):
        pass

    def getJson(self) -> str:
        return "Neutral"
    
    class Neutral(modelsData):
        def __init__(self):
            pass
        
        def getJson(self) -> str:
            return "Neutral"
    
class Manner(Social):
    def __init__(self):
        super().__init__()
    
    class Polite(modelsData):
        def __init__(self):
            pass
        
        def getJson(self) -> str:
            return "Polite"
    
    class Rude(modelsData):
        def __init__(self):
            pass
        
        def getJson(self) -> str:
            return "Rude"

class SocialAnxiety(Social):
    def __init__(self):
        super().__init__()
    
    class Outgoing(modelsData):
        def __init__(self):
            pass
        
        def getJson(self) -> str:
            return "Outgoing"
    
    class Shy(modelsData):
        def __init__(self):
            pass
        
        def getJson(self) -> str:
            return "Shy"

class Optimism(Social):
    def __init__(self):
        super().__init__()
    
    class Negative(modelsData):
        def __init__(self):
            pass
        
        def getJson(self) -> str:
            return "Negative"
    
    class Positive(modelsData):
        def __init__(self):
            pass
        
        def getJson(self) -> str:
            return "Positive"


class HomeRegion(modelsData):
    def __init__(self):
        pass

    def getJson(self) -> str:
        return "Other"
    
    class Town(modelsData):
        def __init__(self):
            pass
        
        def getJson(self) -> str:
            return "Town"
    
    class Desert(modelsData):
        def __init__(self):
            pass
        
        def getJson(self) -> str:
            return "Desert"

    class Other(modelsData):
        def __init__(self):
            pass
        
        def getJson(self) -> str:
            return "Other"


class Calendar(modelsData):
    def __init__(self):
        pass

    def getJson(self) -> str:
        return "AlwaysShown"
    
    
    
    class HiddenAlways(modelsData):
        def __init__(self):
            pass
        
        def getJson(self) -> str:
            return "HiddenAlways"
    
    class HiddenUntilMet(modelsData):
        def __init__(self):
            pass
        
        def getJson(self) -> str:
            return "HiddenUntilMet"
    
    class AlwaysShown(modelsData):
        def __init__(self):
            pass
        
        def getJson(self) -> str:
            return "AlwaysShown"
        

class SocialTab(Calendar):
    def __init__(self):
        super().__init__()
    
    class UnknownUntilMet(modelsData):
        def __init__(self):
            pass
        
        def getJson(self) -> str:
            return "UnknownUntilMet"
    
class EndSlideShow(modelsData):
    def __init__(self):
        pass

    def getJson(self) -> str:
        return "MainGroup"
    
    class Hidden(modelsData):
        def __init__(self):
            pass
        
        def getJson(self) -> str:
            return "Hidden"
        
    class MainGroup(modelsData):
        def __init__(self):
            pass
        
        def getJson(self) -> str:
            return "MainGroup"
    

    class TrailingGroup(modelsData):
        def __init__(self):
            pass
        
        def getJson(self) -> str:
            return "TrailingGroup"
    