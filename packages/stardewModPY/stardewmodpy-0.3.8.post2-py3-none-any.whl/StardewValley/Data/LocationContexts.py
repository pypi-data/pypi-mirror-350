from .model import modelsData
from typing import Optional, Any


class LocationContextsData(modelsData):
    def __init__(
        self,
        key: str,
        AllowRainTotem: Optional[bool] = True,
        RainTotemAffectsContext: Optional[str] = None,
        MaxPassOutCost: Optional[int] = 1000,
        PassOutMail: Optional[list[dict[str, Any]]] = None,
        PassOutLocations: Optional[list[dict[str, Any]]] = None,
        ReviveLocations: Optional[list[dict[str, Any]]] = [{"Id": "Default", "Condition": None, "Location": "Hospital", "Position": {"X": 20, "Y": 12}}],
        SeasonOverride: Optional[str] = None,
        WeatherConditions: Optional[list[dict[str, str]]] = [{"Id": "Default", "Condition": None, "Weather": "Sun"}],
        CopyWeatherFromLocation: Optional[str] = None,
        DefaultMusic: Optional[str] = None,
        DefaultMusicCondition: Optional[str] = None,
        DefaultMusicDelayOneScreen: Optional[bool] = False,
        Music: Optional[list[dict[str, str]]] = [],
        DayAmbience: Optional[str] = None,
        NightAmbience: Optional[str] = None,
        PlayRandomAmbientSounds: Optional[bool] = True,
        CustomFields: Optional[Any] = None
    ):
        super().__init__(key)
        self.AllowRainTotem = AllowRainTotem
        self.RainTotemAffectsContext = RainTotemAffectsContext
        self.MaxPassOutCost = MaxPassOutCost
        self.PassOutMail = PassOutMail
        self.PassOutLocations = PassOutLocations
        self.ReviveLocations = ReviveLocations
        self.SeasonOverride = SeasonOverride
        self.WeatherConditions = WeatherConditions
        self.CopyWeatherFromLocation = CopyWeatherFromLocation
        self.DefaultMusic = DefaultMusic
        self.DefaultMusicCondition = DefaultMusicCondition
        self.DefaultMusicDelayOneScreen = DefaultMusicDelayOneScreen
        self.Music = Music
        self.DayAmbience = DayAmbience
        self.NightAmbience = NightAmbience
        self.PlayRandomAmbientSounds = PlayRandomAmbientSounds
        self.CustomFields = CustomFields
