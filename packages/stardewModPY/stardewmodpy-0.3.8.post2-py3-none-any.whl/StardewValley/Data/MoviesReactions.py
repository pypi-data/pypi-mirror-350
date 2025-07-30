from .model import modelsData


class ReactionData(modelsData):
    def __init__(
        self,
        Tag: str,
        Response: str,
        Whitelist: list[str],
        SpecialResponses: dict[str, dict[str, str | None]],
        Id: str
    ):
        super().__init__(None)
        self.Tag = Tag
        self.Response = Response
        self.Whitelist = Whitelist
        self.SpecialResponses = SpecialResponses
        self.Id = Id


class MoviesReactionsData(modelsData):
    def __init__(
        self,
        NPCName: str,
        Reactions: list[ReactionData],
    ):
        super().__init__(None)
        self.NPCName = NPCName
        self.Reactions = Reactions
