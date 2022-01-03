import os
import os.path
from pathlib import Path
from dataclasses import dataclass
import csv

import rich


@dataclass
class ObjectData:
    obj_id: str
    scale: float
    x: float
    y: float
    z: float
    h: float = 0.0
    p: float = 0.0
    r: float = 0.0
    



class MapPosition:
    
    BASE_DIR = Path(__file__).resolve().parent
    SRC_DIR = BASE_DIR.joinpath('maps')
    
    def __init__(self):
        pass
    
    
    def read(self, filename, obj, names:list):
        filename = MapPosition.SRC_DIR.joinpath(filename)
        fieldnames = ['objid','s','x','y','z','h','p','r']
        objects = []
        with open(filename, newline='') as f:
            reader = csv.DictReader(f, fieldnames=fieldnames, delimiter=';')
            for obj in reader:
                objects.append(ObjectData(*obj.values()))
        return objects



if __name__ == '__main__':
    mappos = MapPosition()
    
    obj = mappos.read('./map.csv', 1, [1,2,3])
    rich.print(obj)


















