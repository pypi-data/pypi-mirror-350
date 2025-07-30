from __future__ import annotations
from ..contentpatcher import EditData

from typing import Optional, List, Any, TYPE_CHECKING
if TYPE_CHECKING:
    from ..helper import Helper

class modelsData:
    def __init__(self, key: str|int):
        self.key=key

    def getJson(self, useGetStr:Optional[list[str]]=None) -> dict: #customized because of getStr functions
        json = {}
        useGetStr = useGetStr or []
        for attr, value in vars(self).items():
            if value is not None and attr not in ["key"]:
                if isinstance(value, list):
                    new_list  = []
                    for item in value:
                        if not isinstance(item, (str, int, float, bool, list, dict, tuple, set)):
                            if hasattr(item, "getStr") and attr in useGetStr and callable(item.getStr):
                                new_list.append(item.getStr())
                            elif hasattr(item, "getJson") and callable(item.getJson):
                                new_list.append(item.getJson())
                            else:
                                raise TypeError(f"Item da lista '{attr}' é uma classe personalizada sem getJson/getStr")
                        else:
                            new_list.append(item)
                    json[attr] = new_list
                if not isinstance(value, (str, int, float, bool, list, dict, tuple, set)):
                    if hasattr(value, "getStr") and attr in useGetStr and callable(value.getStr):
                        json[attr] = value.getStr()
                    elif hasattr(value, "getJson") and callable(value.getJson):
                        json[attr] = value.getJson()
                    else:
                        raise TypeError(f"Variable '{attr}' is a custom class but has neither getJson() nor getStr()")
                else:
                    json[attr] = value
        
        return json
    
    def register(self, LogName:str, Target:str, mod:Helper, contentFile:Optional[str]="content"):
        
        if self.key is None:
            raise ValueError("key cannot be None, this class not registry in object game content.")
        
        key=self.key
        value=self.getJson()
        mod.content.registryContentData(
            EditData(
                LogName=LogName,
                Target=Target,
                Entries={
                    # Mapeia a chave do seu objeto para a representação JSON do objeto
                    self.key: self.getJson()
                }
            ),
            contentFile=contentFile
        )