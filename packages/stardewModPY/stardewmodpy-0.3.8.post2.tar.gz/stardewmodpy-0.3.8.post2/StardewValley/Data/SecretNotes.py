from .model import modelsData


class SecretNotesData(modelsData):
    def __init__(self, key: str, text: str):
        super().__init__(key)
        self.text = text


    def getJson(self) -> dict:
        return {"text": self.text}
