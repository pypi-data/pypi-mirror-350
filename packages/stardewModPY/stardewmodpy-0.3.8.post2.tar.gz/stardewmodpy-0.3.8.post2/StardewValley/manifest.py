from typing import List, Optional

class Manifest:
    def __init__(self, Name: str, Author: str, Version: str, Description: str, UniqueID: str, UpdateKeys: List[str] = [],
                 ContentPackFor: Optional[dict] = None):
        self.Name = Name
        self.Author = Author
        self.Version = Version
        self.Description = Description
        self.UniqueID = UniqueID
        self.UpdateKeys = UpdateKeys if UpdateKeys is not None else []
        self.ContentPackFor = ContentPackFor if ContentPackFor is not None else {}
    
    def json(self):
        return{
            "Name":self.Name,
            "Author":self.Author,
            "Version": self.Version,
            "Description": self.Description,
            "UniqueID": self.UniqueID,
            "UpdateKeys": self.UpdateKeys,
            "ContentPackFor": self.ContentPackFor
        }
