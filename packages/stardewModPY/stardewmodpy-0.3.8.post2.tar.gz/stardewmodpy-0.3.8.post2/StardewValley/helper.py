from .verification import steamLoad
from .contentpatcher import ContentPatcher
from .slingshot import SlingShotFramework
from .FTM.farmtypemanager import FarmTypeManager
from .manifest import Manifest
from .jsonreader import jsonStardewRead
import os, shutil, subprocess, platform
from typing import Optional

class i18n:
    def __init__(self):
        self.json={
            "default":{},
            "de":{},
            "es":{},
            "fr":{},
            "it":{},
            "ja":{},
            "ko":{},
            "hu":{},
            "pt":{},
            "ru":{},
            "tr":{},
            "zh":{}
        }
    

class Helper:
    def __init__(self, manifest:Manifest, modFramework:Optional[ContentPatcher|SlingShotFramework|FarmTypeManager]=None):
        self.modFolderAssets=os.path.join(os.getcwd(), "assets")
        self.assetsFileIgnore=[]
        if modFramework is None:
            self.content = ContentPatcher(manifest=manifest)
        else:
            self.content = modFramework
        
        self.i18n=i18n()
        steamVerify=steamLoad()
        self.pathSteam=steamVerify.verify()
        self.jsonRead=jsonStardewRead()
    
    def sdk(self, assetFolder:str, assetObject:str):
        sdkPath=os.path.join(self.pathSteam, "Content (unpacked)", assetFolder, assetObject+".json")
        return self.jsonRead.read_json(sdkPath)


    def translation(self, language:str, key:str, value:str):
        self.i18n.json[language].update({key:value})

    def _ignore_files(self, dir, files):
        ignored = []
        for file in files:
            full_path = os.path.join(dir, file)
            rel_path = os.path.relpath(full_path, self.modFolderAssets)
            rel_path = rel_path.replace("\\", "/")
            if rel_path in self.assetsFileIgnore:
                ignored.append(file)
        return ignored
    
    def write(self, run:bool=False):
        modPath=os.path.join(self.pathSteam, "Mods", self.content.Manifest.Name)
        if os.path.exists(modPath):
            shutil.rmtree(modPath)
        if not os.path.exists(modPath):
            os.makedirs(modPath)
            if isinstance(self.content, ContentPatcher):
                if(os.path.exists(self.modFolderAssets)):
                    shutil.copytree(self.modFolderAssets,os.path.join(modPath, "assets"), ignore=self._ignore_files)

        if isinstance(self.content, ContentPatcher):
            i18nPath=os.path.join(modPath, "i18n")

            if not os.path.exists(i18nPath):
                os.makedirs(i18nPath)
                for key, value in self.i18n.json.items():
                    self.jsonRead.write_json(os.path.join(i18nPath, f"{key}.json"), value)
        
            
        self.jsonRead.write_json(os.path.join(modPath, "manifest.json"), self.content.Manifest.json())
        self.jsonRead.write_json(os.path.join(modPath, self.content.fileName), self.content.contentFile)
        
        if isinstance(self.content, ContentPatcher):
            for key, value in self.content.contentFiles.items():            
                self.jsonRead.write_json(os.path.join(modPath, "assets", f"{key}.json"), value)
            

        try:
            if run:
                subprocess.run(os.path.join(self.pathSteam, "StardewModdingApi.exe" if platform.system() == 'Windows' else "StardewModdingAPI"), check=True)
            
        except Exception as e:
            print(f"Erro ao iniciar o jogo {e}")