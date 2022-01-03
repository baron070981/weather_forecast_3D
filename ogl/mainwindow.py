from direct.showbase.ShowBase import ShowBase
from direct.actor.Actor import Actor
from panda3d.core import ModelNode
from panda3d.core import Loader
from panda3d.core import Filename, AmbientLight, DirectionalLight
from panda3d.core import loadPrcFileData
from panda3d.core import KeyboardButton
from panda3d.core import LPoint3, LVector3, TextureStage, TexGenAttrib
from direct.filter.CommonFilters import CommonFilters


import sys
import gltf
import math
from math import cos, sin

try:
    from . import surrounding_objects as surobj
    from . import lights
    from . import position_map_proc as pmp
except:
    import surrounding_objects as surobj
    import lights
    import position_map_proc as pmp



loadPrcFileData('', 'win-size 1280 700') # утсановка размера окна 1280 Х 700

map_houses = pmp.MapPosition().read('./map.csv', 1, 1) # загрузка позиций для размещения домов


class World(ShowBase):
    
    
    def __init__(self, **kwargs):
        ShowBase.__init__(self)
        
        self.lightcolor = (0.7, 0.7, 0.7, 1)
        self.state_color_plus = True
        
        self.angle = 0.0 # угол поворота камеры по оси X
        self.a_y = 0.0 # угол поворота камеры по оси y
        self.a_z = 0.0 # угол поворота камеры по оси z
        
        self.x = 0.0
        self.y = -200
        self.z = 0.7
        
        
        self.vec_dir = (0,1)
        
        self.speed = 1.5
        
        self.speed_vec = (0.1, 0.1)
        
        self.position = (self.x, self.y, self.z) # позиция камеры
        self.cam.set_pos(self.position)
        
        self.filters = CommonFilters(self.win, self.cam)
        
        
        self.forward = KeyboardButton.ascii_key('w')
        self.backward = KeyboardButton.ascii_key('s')
        self.left = KeyboardButton.ascii_key('a')
        self.right = KeyboardButton.ascii_key('d')
        self.red = KeyboardButton.ascii_key('r')
        self.green = KeyboardButton.ascii_key('g')
        self.blue = KeyboardButton.ascii_key('b')
        self.color_plus = KeyboardButton.ascii_key('p')
        self.color_minus = KeyboardButton.ascii_key('m')
        
        self.toleft = KeyboardButton.left()
        self.toright = KeyboardButton.right()
        self.toup = KeyboardButton.up()
        self.todown = KeyboardButton.down()
        
        
        # self.win.setClearColor((0.3, 0, 0, 1))
        self.set_background_color(0.0, 0.5, 0.75, 1)
        
        
        
        self.sky = surobj.SkyBox('cubemap', 'bigcube.glb', 'sky_#.png')
        self.sky.obj.setScale(2.1)
        self.sky.obj.setY(0.)
        self.sky.obj.setX(0.)
        self.sky.obj.setZ(0)
        
        
        self.land = surobj.ModelObj('landscape_summer.glb', rot=(0, 180, 0), position=(0,0,6))
        self.land.obj.setScale(2)
        self.land.obj.setY(0.)
        self.land.obj.setX(0.)
        self.land.obj.setZ(-1)
        self.land.obj.setR(180)
        # self.land.obj.setP(180)
        
        houses = []
        for house in map_houses:
            h = surobj.ModelObj('wooden_house_sum.glb')
            h.obj.setScale(float(house.scale))
            h.obj.setY(float(house.y))
            h.obj.setX(float(house.x))
            h.obj.setZ(float(house.z))
            h.obj.setR(float(house.r))
            h.obj.setH(float(house.h))
            h.name = house.obj_id
            houses.append(h)
        
        # self.izba = surobj.ModelObj('wooden_house_sum.glb', rot=(0, 180, 0), position=(0,0,6))
        # self.izba.obj.setScale(1.5)
        # self.izba.obj.setY(120.)
        # self.izba.obj.setX(30.)
        # self.izba.obj.setZ(-0.8)
        # self.izba.obj.setR(180)
        # self.izba.obj.setH(-170)
        
        
        
        
        self.ambientLight = lights.TotalLight((0.5, 0.4, 0.3, 1))
        render.setLight(render.attachNewNode(self.ambientLight.obj))
        
        
        
        
        self.directlight = lights.LocalLight(color=(1,0,0,1),pos=(100, -100, 100),dirpos=(-400, 200, -3))
        # self.directlight.add('izba', self.izba.obj)
        for house in houses:
            self.directlight.add(house.name, house.obj)
        self.directlight.add('land', self.land.obj)
        
        
        self.setFrameRateMeter(True)
        
        
        
        self.accept('r', self.move_task, [self.red])
        self.accept('g', self.move_task, [self.green])
        self.accept('b', self.move_task, [self.blue])
        self.accept('p', self.move_task, [self.color_plus])
        self.accept('m', self.move_task, [self.color_minus])
        # self.accept('p-repeat', self.move_task, [self.forward])
        # self.accept('m-repeat', self.move_task, [self.forward])
        
        
        self.accept("escape", sys.exit)
        self.accept('w-repeat', self.move_task, [self.forward])
        self.accept('s-repeat', self.move_task, [self.backward])
        self.accept('a-repeat', self.move_task, [self.left])
        self.accept('d-repeat', self.move_task, [self.right])
        self.accept('arrow_left-repeat', self.move_task, [self.toleft])
        self.accept('arrow_right-repeat', self.move_task, [self.toright])
        self.accept('arrow_up-repeat', self.move_task, [self.toup])
        self.accept('arrow_down-repeat', self.move_task, [self.todown])
    
    
    
    # поворот по оси X
    def rotate(self, angle = 1):
        # self.angle += angle
        # self.cam.lookAt(self.angle, self.a_y, self.a_z)
        hpr = self.cam.getHpr()
        self.angle = hpr[0]+angle
        self.cam.setH(self.angle)
        print(self.cam.getH())
    
    
    def vertical_rotate(self, angle = 0.3):
        hpr = self.cam.getHpr()
        self.a_y = hpr[1]+angle
        self.cam.setP(self.a_y)
        print(self.cam.getP())
    
    
    # перемещение камеры назад
    def move_forward(self, distance=1):
        x, y, z = self.cam.getPos()
        angle = (self.angle+90) * math.pi / 180
        x += cos(angle)*distance
        y += sin(angle)*distance
        self.x = x
        self.y = y
        print(f'X: {x}, Y: {y}, A: {self.angle}\n  Cos: {round(cos(self.angle), 3)}, Sin: {round(sin(self.angle), 2)}')
        self.cam.setX(self.x)
        self.cam.setY(self.y)
    
    
    # перемещение камеры назад
    def move_backward(self, distance=1):
        x, y, z = self.cam.getPos()
        angle = (self.angle-90) * math.pi / 180
        x += cos(angle)*distance
        y += sin(angle)*distance
        self.x = x
        self.y = y
        print(f'X: {x}, Y: {y}, A: {self.angle}\n  Cos: {round(cos(self.angle), 3)}, Sin: {round(sin(self.angle), 2)}')
        self.cam.setX(self.x)
        self.cam.setY(self.y)
    
    
    # перемещение камеры влево
    def move_left(self, distance=1):
        x, y, z = self.cam.getPos()
        angle = (self.angle+180) * math.pi / 180
        x += cos(angle)*distance
        y += sin(angle)*distance
        self.x = x
        self.y = y
        print(f'X: {x}, Y: {y}, A: {self.angle}\n  Cos: {round(cos(self.angle), 3)}, Sin: {round(sin(self.angle), 2)}')
        self.cam.setX(self.x)
        self.cam.setY(self.y)
    
    
    # перемещение камеры вправо
    def move_right(self, distance=1):
        x, y, z = self.cam.getPos()
        angle = (self.angle) * math.pi / 180
        x += cos(angle)*distance
        y += sin(angle)*distance
        self.x = x
        self.y = y
        print(f'X: {x}, Y: {y}, A: {self.angle}\n  Cos: {round(cos(self.angle), 3)}, Sin: {round(sin(self.angle), 2)}')
        self.cam.setX(self.x)
        self.cam.setY(self.y)
    
    
    
    
    # обработка нажатия клавиатуры
    def move_task(self, key):
        
        # Check if the player is holding W or S
        is_down = base.mouseWatcherNode.is_button_down
        
        
        # нажата клавиша W
        if is_down(self.forward):
            self.move_forward(self.speed)
        
        # нажата клавиша S
        if is_down(self.backward):
            self.move_backward(self.speed)

        # нажата клавиша A
        if is_down(self.left):
            self.move_left(self.speed)
        
        # нажата клавиша D
        if is_down(self.right):
            self.move_right(self.speed)
        
        #  нажата клавиша стрелка влево
        if is_down(self.toleft):
            self.rotate(1)
        
        #  нажата клавиша стрелка вправо
        if is_down(self.toright):
            self.rotate(-1)
        
        #  нажата клавиша стрелка вправо
        if is_down(self.toup):
            self.vertical_rotate(0.3)
        
        #  нажата клавиша стрелка вправо
        if is_down(self.todown):
            self.vertical_rotate(-0.3)
            
        if is_down(self.red):
            self.ambientLight.set_color(color='red')
            
        if is_down(self.green):
            self.ambientLight.set_color(color='green')
            
        if is_down(self.blue):
            self.ambientLight.set_color(color='blue')
            
        if is_down(self.color_plus):
            self.ambientLight.set_flag(True)
            
        if is_down(self.color_minus):
            self.ambientLight.set_flag(False)
        
        # self.cam.lookAt(point=LPoint3(0, 100, -10), up=(0,0,1))
    
    
    
    
    def update(self):
        # slef.angle, self.position, self.vec_dir
        ...


if __name__ == '__main__':

    world = World()
    world.run()








