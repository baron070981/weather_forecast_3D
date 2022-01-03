from direct.showbase.ShowBase import ShowBase
from direct.actor.Actor import Actor
from panda3d.core import ModelNode
from panda3d.core import Loader
from panda3d.core import Filename, AmbientLight, DirectionalLight
from panda3d.core import loadPrcFileData
from panda3d.core import KeyboardButton
from panda3d.core import LPoint3, LVector3, LColor

import datetime
import time


class TotalLight:
    
    def __init__(self, color=(0.1, 0.1, 0.1, 1)):
        self.lightcolor = LColor(color)
        self.obj = AmbientLight("ambientLight")
        self.obj.setColor(self.lightcolor)
        self.step_color = 0.01
        self.CHOICE_OPERATION = True
    
    
    @property
    def invert_flag(self):
        self.CHOICE_OPERATION = not self.CHOICE_OPERATION
    
    
    def set_flag(self, state:bool):
        self.CHOICE_OPERATION = state
    
    
    def set_color(self, color):
        def check_value(val):
            if val > 1:
                return 1
            elif val < 0:
                return 0
            return val
        
        r, g, b, a = self.lightcolor
        
        if color == 'red':
            if self.CHOICE_OPERATION:
                r += self.step_color
            else:
                r -= self.step_color
            r = check_value(r)
        elif color == 'green':
            if self.CHOICE_OPERATION:
                g += self.step_color
            else:
                g -= self.step_color
            g = check_value(g)
        elif color == 'blue':
            if self.CHOICE_OPERATION:
                b += self.step_color
            else:
                b -= self.step_color
            b = check_value(b)
        self.lightcolor = (r,g,b,a)
        self.obj.setColor(self.lightcolor)



class LocalLight:
    
    def __init__(self, color=(1,1,1,1), pos=(0,0,0), dirpos=(0,0,0)):
        self.objects = {}
        self.color = LColor(color)
        self.position = pos
        self.direction = dirpos
        self.specular = (0.1, 0.1, 0.1, 1)
        
        self.obj = DirectionalLight("directionalLight")
        self.obj.setPoint(self.position)
        self.obj.setDirection(self.direction)
        self.obj.setColor((1, 0, 0, 1))
        self.obj.setSpecularColor(self.specular)
        
        self.light = render.attachNewNode(self.obj)
    
    
    def set_specular(self, color):
        self.specular = color
    
    
    def add(self, name, node):
        self.objects[name] = node
        node.setLight(self.light)
    
    
    def remove(self, node_name):
        ...





class Solaris(LocalLight):
    
    '''
    класс расчета положения солнца по заданному времени и создание источника света 
    в расчитанной позиции.
    '''
    
    def __init__(self, color=(1,1,1,1), pos=(0,0,0), dirpos=(0,0,0)):
        super().__init__(color=color, pos=pos, dirpos=dirpos)
        
        self.timeintervals = ...
    
    
    def __round_time(self, t):
        '''
        t - строка формата HH.MM
        '''
        h = m = None
        if isinstance(t, str):
            h, m = list(map(int, t.split('.')))
        if isinstance(t, time):
            h = t.tm_hour
            m = t.tm_min
        else:
            raise Exception('Не верный тип аргумента t')
        if m > 30:
            h += 1
        return h
    
    
    def __calculate_percentes(self, sunrise):
        return int(round((12 - (sunrise+1))*30/100)) + sunrise+1
    
    
    def __set_time_intervals(self, sunrise, sunset):
        '''
        timeintervals - {1:[sunrise, t2], 2:[t2, t3], ..., n:[t, sunset]}
        '''
        sunrise = self.__round_time(sunrise)
        sunseet = self.__round_time(sunset)
        self.timeintervals[1] = [sunrise, sunrise+1]
        self.timeintervals[2] = [sunrise+1, ]
    
    
    def test_time(self, t, sunrise, sunset):
        ...



if __name__ == '__main__':
    t = time.strptime('22.39.37', '%H.%M.%S')
    print(t)

















