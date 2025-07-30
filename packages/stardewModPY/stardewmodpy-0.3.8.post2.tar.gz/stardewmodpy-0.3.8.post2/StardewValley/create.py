import sys, os
from .projectlibs import colorize
import subprocess

def main():
    if os.name == 'nt':
        os.system('')

    cores=colorize()
    if len(sys.argv) == 2 and sys.argv[1]=="run":
        print(f"{cores.colorize(cores.green)}Iniciando o Projeto:{cores.reset()}")
        if os.path.exists("main.py"):
            subprocess.run([sys.executable, "main.py"])
        else:
            print(f"{cores.colorize(cores.red)}main.py não encontrado no diretório atual.{cores.reset()}")

        return

    if len(sys.argv) <6:        
        comandos={
            "Create a project:":cores.green,
            "sdvpy":cores.white,
            "create": cores.green,
            "<modname>":cores.cyan,
            "<author>":cores.yellow,
            "<version>":cores.cyan,
            "<description>":cores.red
        }
        print(f"{' '.join(f'{cores.colorize(i)}{item}' for item, i in comandos.items())}{cores.reset()}")
        return
    
    modName=sys.argv[2]
    author=sys.argv[3]
    version=sys.argv[4]
    description=sys.argv[5]

    if os.path.exists(modName):
        print(f"{cores.colorize(cores.red)}There is already a project or folder with that name, delete it or choose another name{cores.reset()}")
        return
    
    os.makedirs(modName)
    mod_entry_path = os.path.join(modName, "ModEntry.py")
    content = f"""from StardewValley import Manifest
from StardewValley.helper import Helper

class ModEntry(Helper):
    def __init__(self):
        super().__init__(Manifest(
            "{modName}",
            "{author}",
            "{version}",
            "{description}",
            "{author}.{modName}"
        ))
        self.contents()
    
    def contents(self):
        #Mod Content
        ...

"""
    with open(mod_entry_path, "w", encoding="utf-8") as f:
        f.write(content)
    
    main_path = os.path.join(modName, "main.py")
    mainContent=f"""from ModEntry import ModEntry

mod=ModEntry()
mod.write()
"""
    with open(main_path, "w", encoding="utf-8") as f:
        f.write(mainContent)
