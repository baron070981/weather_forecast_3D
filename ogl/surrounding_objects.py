from direct.showbase.ShowBase import ShowBase
from direct.actor.Actor import Actor
from panda3d.core import ModelNode
from panda3d.core import Loader
from panda3d.core import Filename, AmbientLight, DirectionalLight
from panda3d.core import loadPrcFileData
from panda3d.core import KeyboardButton
from panda3d.core import LPoint3, LVector3, TextureStage, TexGenAttrib


import sys
import gltf
import math
from math import cos, sin
from pathlib import Path
import os, os.path


class SkyBox:
    '''
    модель куба и текстуры для него должны находиться в 
    одной папке,отдельно от других моделей
    '''
    BASE_DIR = Path(__file__).resolve().parent
    SRC_DIR = BASE_DIR.joinpath('src')
    
    def __init__(self, dirname, model_name, tex_name, position = (0,-1,0), rot=(0,0,0)):
        '''
        dirname - имя папки в которой находятся модель куба и текстуры
                  сама папка должна находиться по пути ..../ogl/src/
        model_name - имя файла модели
        tex_name - имя текстуры, например tex_#
        '''
        
        # определение путей
        self.dirname = SkyBox.SRC_DIR.joinpath(Path(dirname))
        self.model_name = self.dirname.joinpath(model_name)
        self.texname = self.dirname.joinpath(tex_name)
        
        # загрузка текстур
        self.tex = loader.loadCubeMap(self.texname)
        
        # загрузка модели куба
        self.obj = loader.loadModel(self.model_name)
        
        # установка текстур
        self.obj.setTexGen(TextureStage.getDefault(), TexGenAttrib.MWorldPosition)
        self.obj.setTexture(self.tex)
        
        # подключение к рендеру
        self.obj.reparentTo(render)
        
        # установка начальных параметров
        self.obj.setPos(position)
        self.obj.setHpr(rot)
        self.x, self.y, self.z = position
        self.position = (self.x, self.y, self.z)
    
    
    
    def update_pos(self, position):
        x, y, z = position
        self.x += x
        self.y += y
        self.z += z
        self.position = (self.x, self.y, self.z)
        self.obj.setPos(self.position)



class ModelObj:
    
    BASE_DIR = Path(__file__).resolve().parent
    SRC_DIR = BASE_DIR.joinpath('src/models/')
    
    def __init__(self, model_name, position = (0,-1,0), rot=(0,0,0)):
        self.model_name = ModelObj.SRC_DIR.joinpath(model_name)
        self.obj = loader.loadModel(self.model_name)
        self.obj.reparentTo(render)
        self.obj.setPos(position)
        self.obj.setHpr(rot)
        self.name = ''























